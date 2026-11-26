"""Structured logging with structlog, one JSON line per event in production.

Every request gets a new request id (a client's X-Request-ID header is never used: it could
carry personal data), bound to all log lines for that request and echoed in the response header,
and one access line when it ends. Exception messages are never logged (decision 0014).
Logs from the standard library (uvicorn, httpx) go through the same renderer, so production
output is JSON throughout.
"""

from __future__ import annotations

import logging
import sys
import time
import uuid
from collections.abc import Awaitable, Callable
from typing import Any, TextIO

import structlog
from fastapi import Request, Response
from structlog.tracebacks import ExceptionDictTransformer

from vestagraph_api.settings import Settings

REQUEST_ID_HEADER = "X-Request-ID"
log = structlog.get_logger()


def _scrub(stacks: Any) -> Any:
    # Keep each exception's type and its frames (file, line, function); drop the message, the
    # notes and a SyntaxError's source line, which can all hold request data. Exception groups
    # nest further lists of stacks.
    if isinstance(stacks, list):
        return [_scrub(item) for item in stacks]
    if isinstance(stacks, dict):
        cleaned = {k: _scrub(v) for k, v in stacks.items() if k not in ("exc_value", "exc_notes")}
        cleaned["exc_value"] = ""
        cleaned["exc_notes"] = []
        if "syntax_error" in cleaned:
            cleaned["syntax_error"] = None
        return cleaned
    return stacks


class _NoMessageTransformer(ExceptionDictTransformer):
    """The structured traceback without any exception message, for the whole exception chain.
    `show_locals` is off for the same reason: locals can hold request data or credentials."""

    def __init__(self) -> None:
        super().__init__(show_locals=False)

    def __call__(self, exc_info: Any) -> list[dict[str, Any]]:
        scrubbed: list[dict[str, Any]] = _scrub(super().__call__(exc_info))
        return scrubbed


def _console_traceback(sio: TextIO, exc_info: Any) -> None:
    def write(stacks: list[dict[str, Any]], indent: str) -> None:
        for stack in stacks:
            sio.write(f"{indent}{stack['exc_type']}\n")
            for frame in stack["frames"]:
                sio.write(f"{indent}  {frame['filename']}:{frame['lineno']} in {frame['name']}\n")
            for group in stack.get("exceptions", []):
                write(group, indent + "    ")

    write(_NoMessageTransformer()(exc_info), "")


def configure_logging(settings: Settings) -> None:
    # JSON lines carry tracebacks as structured data, the console as plain text. Both keep the
    # exception types and frame locations and drop the messages (_NoMessageTransformer).
    rendering: list[structlog.types.Processor] = (
        [
            structlog.processors.ExceptionRenderer(_NoMessageTransformer()),
            structlog.processors.JSONRenderer(),
        ]
        if settings.log_json
        else [structlog.dev.ConsoleRenderer(exception_formatter=_console_traceback)]
    )
    shared: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]
    level = logging.getLevelNamesMapping()[settings.log_level]
    structlog.configure(
        processors=[*shared, *rendering],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.PrintLoggerFactory(),
    )
    _route_stdlib_logging(shared, rendering, level)


class _NotTheDuplicateTraceback(logging.Filter):
    # The app's 500 handler has already logged the error with its request id; uvicorn then logs
    # the same exception again, as plain text without one, when Starlette re-raises it.
    def filter(self, record: logging.LogRecord) -> bool:
        return not record.getMessage().startswith("Exception in ASGI application")


def _route_stdlib_logging(
    shared: list[structlog.types.Processor],
    rendering: list[structlog.types.Processor],
    level: int,
) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=shared,
            processors=[structlog.stdlib.ProcessorFormatter.remove_processors_meta, *rendering],
        )
    )
    handler.addFilter(_NotTheDuplicateTraceback())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
    # uvicorn (`fastapi run`) installs its own plain-text handlers before the app is imported:
    # send its logs to the root handler instead. Its access log is replaced by request_context's.
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.propagate = True
    logging.getLogger("uvicorn.access").disabled = True
    # A line per outgoing HTTP request is noise at INFO.
    for name in ("httpx", "httpcore", "urllib3"):
        logging.getLogger(name).setLevel(max(level, logging.WARNING))


async def request_context(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = uuid.uuid4().hex
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)
    # Kept on the request too: the 500 handler runs outside this middleware and adds it itself.
    request.state.request_id = request_id
    started = time.perf_counter()
    response = await call_next(request)
    response.headers[REQUEST_ID_HEADER] = request_id
    # The route's template (/api/area-check), not the path: ids and other values in URLs
    # stay out of the logs. Unhandled errors are logged by the 500 handler instead.
    route = request.scope.get("route")
    log.info(
        "request",
        method=request.method,
        route=getattr(route, "path", None),
        status=response.status_code,
        duration_ms=round((time.perf_counter() - started) * 1000),
    )
    return response
