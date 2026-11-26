"""POST /api/area-check: the area answer for one typed postcode.

The answer comes from ``vestagraph_area`` (the same functions that make ``area-result.json``);
nothing is calculated here (AGENTS rule 2). A found answer quotes that postcode's records from
``postcode-area.json`` as they are, with their source, date and level. An unknown postcode carries
no facts at all (rule 7). The request is never logged and never echoed (decision 0014).

The route stays closed (503, before the body is read) until ``AREA_CHECK_OPEN`` is on.
"""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any, Literal

from fastapi import APIRouter, Request, Response
from fastapi.routing import APIRoute
from pydantic import BaseModel, Field, WithJsonSchema
from vestagraph_area.area_check import check_postcode, postcode_result
from vestagraph_area.records import (
    PostcodeArea,
    Priority,
    Registry,
    read_postcode_area,
    read_registry,
    read_sample_priorities,
)

from vestagraph_api.contract_schemas import RECORD_SCHEMA, RESULT_SCHEMA
from vestagraph_api.problems import (
    MEDIA_TYPE,
    Problem,
    ProblemDetails,
    ValidationProblem,
    problem_schema,
)


@dataclass(frozen=True, slots=True)
class AreaData:
    """The three data files, read once when the app starts."""

    registry: Registry
    area: PostcodeArea
    priorities: tuple[Priority, ...]
    raw_records: dict[str, list[dict[str, Any]]]


def load_area_data(fixtures_dir: Path) -> AreaData:
    data = fixtures_dir / "data"
    registry = read_registry(data / "pilot-topics.json")
    area = read_postcode_area(data / "postcode-area.json")
    priorities = read_sample_priorities(data / "sample-priorities.json", registry)
    document = json.loads((data / "postcode-area.json").read_text(encoding="utf-8"))
    raw_records: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in document["area"]:
        raw_records[record["postcode"]].append(record)
    return AreaData(registry, area, priorities, dict(raw_records))


class AreaCheckRequest(BaseModel):
    postcode: str = Field(min_length=1, max_length=16)


# The shapes come from the fixtures' JSON Schemas (the single source), for the OpenAPI description
# only: at run time the values pass through as they are.
AreaResult = Annotated[dict[str, Any], WithJsonSchema(RESULT_SCHEMA)]
AreaRecord = Annotated[dict[str, Any], WithJsonSchema(RECORD_SCHEMA)]


class Found(BaseModel):
    state: Literal["found"]
    postcode: str
    nation: Literal["england"]
    result: AreaResult
    records: list[AreaRecord]


class NotFound(BaseModel):
    state: Literal["notFound"]


class NotCovered(BaseModel):
    state: Literal["notCovered"]
    nation: Literal["wales", "scotland", "northern-ireland"]


AreaCheckResponse = Annotated[Found | NotFound | NotCovered, Field(discriminator="state")]


class ClosedUntilOpen(APIRoute):
    """Answers 503 before FastAPI reads or parses the body, while the area check is closed."""

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        handler = super().get_route_handler()

        async def guarded(request: Request) -> Response:
            if not request.app.state.settings.area_check_open:
                raise Problem(
                    503,
                    type_="https://vestagraph.com/problems/not-available-yet",
                    title="Not available yet",
                )
            return await handler(request)

        return guarded


router = APIRouter(prefix="/api", tags=["area"], route_class=ClosedUntilOpen)


@router.post(
    "/area-check",
    response_model=AreaCheckResponse,
    responses={
        422: {
            "description": "The request is not valid: says where and why, never the value.",
            "content": {MEDIA_TYPE: {"schema": problem_schema(ValidationProblem)}},
        },
        503: {
            "description": "The area check is not open yet (title: Not available yet).",
            "content": {MEDIA_TYPE: {"schema": problem_schema(ProblemDetails)}},
        },
    },
)
async def area_check(body: AreaCheckRequest, request: Request) -> Found | NotFound | NotCovered:
    data: AreaData = request.app.state.area
    lookup = check_postcode(data.area, body.postcode)
    if lookup.state == "notFound":
        return NotFound(state="notFound")
    assert lookup.postcode is not None  # noqa: S101 - set whenever the state is not notFound
    assert lookup.nation is not None  # noqa: S101
    if lookup.state == "notCovered":
        return NotCovered(state="notCovered", nation=lookup.nation)
    return Found(
        state="found",
        postcode=lookup.postcode,
        nation="england",
        result=postcode_result(data.registry, data.area, data.priorities, lookup.postcode),
        records=data.raw_records.get(lookup.postcode, []),
    )
