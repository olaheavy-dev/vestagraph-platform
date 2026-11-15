"""Council tax band amounts (City Explorer).

The yearly amount per band is published by the council and recorded in ``council-area.json``
(whole pence, an input with its source, AGENTS rule 2). Only the monthly figure is calculated, by
the cost engine's own ``annual_to_monthly``: divided by 12, rounded once, halves away from zero.
A gap is never shown as 0 (rule 7).
"""

from vestagraph_engine.pence import Pence

from vestagraph_area.council_records import BAND_LETTERS, Fact
from vestagraph_area.records import InvalidAreaDataError


def band_yearly(bands: Fact, band: str) -> Pence | None:
    """The published yearly amount for ``band``, or ``None`` when the council's bands are a gap."""
    if band not in BAND_LETTERS:
        message = f"'{band}' is not a council tax band; the bands are A to H."
        raise InvalidAreaDataError(message)
    if bands.status != "recorded":
        return None
    return Pence(bands.value[band])


def band_monthly(yearly: Pence) -> Pence:
    """The monthly amount: yearly divided by 12, rounded once."""
    return yearly.annual_to_monthly()
