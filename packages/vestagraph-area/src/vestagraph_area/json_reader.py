"""Reads one JSON data file strictly, and checks the fields of its objects.

Shared by the area readers (``records``, ``council_records`` and ``energy_certificate``) and
the generator's energy reader. Decimals are read as exact
``Fraction`` values, so no ``float`` is ever made (AGENTS rule 2); ``NaN``, ``Infinity``, numbers
with an exponent, duplicate keys, bad UTF-8 and JSON nested too deeply are refused. Anything
refused is an ``InvalidAreaDataError``.
"""

import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


class InvalidAreaDataError(ValueError):
    """A data file holds something the reader does not understand."""


# A limit is typed as plain ASCII digits with an optional decimal part: no sign, no spaces, no
# exponent, no fraction bar and no other script's digits.
PLAIN_DECIMAL = re.compile(r"[0-9]+(\.[0-9]+)?", re.ASCII)


def _refuse_constant(text: str) -> object:
    message = f"it holds {text}, which is not a number the reader accepts."
    raise InvalidAreaDataError(message)


def _exact_decimal(text: str) -> Fraction:
    if "e" in text or "E" in text:
        message = f"the number {text} has an exponent; write it as a plain decimal."
        raise InvalidAreaDataError(message)
    return Fraction(text)


def _unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            message = f"the key '{key}' appears twice in one object."
            raise InvalidAreaDataError(message)
        obj[key] = value
    return obj


def load_json_object(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
        parsed = json.loads(
            text,
            parse_float=_exact_decimal,
            parse_constant=_refuse_constant,
            object_pairs_hook=_unique_keys,
        )
    except UnicodeDecodeError as error:
        message = f"{path.name} is not valid UTF-8 text: {error}"
        raise InvalidAreaDataError(message) from error
    except InvalidAreaDataError as error:
        message = f"{path.name}: {error}"
        raise InvalidAreaDataError(message) from error
    except RecursionError as error:
        message = f"{path.name} is nested too deeply to read."
        raise InvalidAreaDataError(message) from error
    except ValueError as error:
        # Bad JSON, or a whole number with more digits than Python converts (4300).
        message = f"{path.name} is not valid JSON: {error}"
        raise InvalidAreaDataError(message) from error
    if not isinstance(parsed, dict):
        message = f"{path.name} must hold a JSON object."
        raise InvalidAreaDataError(message)
    return parsed


def get_field(obj: dict[str, Any], key: str, kind: type, where: str) -> Any:
    if key not in obj:
        message = f"{where}: required field '{key}' is missing."
        raise InvalidAreaDataError(message)
    value = obj[key]
    if not isinstance(value, kind) or (kind is int and isinstance(value, bool)):
        message = f"{where}: field '{key}' must be a {kind.__name__}."
        raise InvalidAreaDataError(message)
    return value


def string_list(obj: dict[str, Any], key: str, where: str, *, required: bool) -> tuple[str, ...]:
    if key not in obj and not required:
        return ()
    items = get_field(obj, key, list, where)
    if not all(isinstance(item, str) for item in items):
        message = f"{where}: field '{key}' must be a list of strings."
        raise InvalidAreaDataError(message)
    return tuple(items)


def object_list(obj: dict[str, Any], key: str, where: str) -> list[dict[str, Any]]:
    items: list[Any] = get_field(obj, key, list, where)
    objects: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            message = f"{where}: every entry of '{key}' must be an object."
            raise InvalidAreaDataError(message)
        objects.append(item)
    return objects


def optional_string(obj: dict[str, Any], key: str, where: str) -> str | None:
    if key not in obj:
        return None
    return str(get_field(obj, key, str, where))
