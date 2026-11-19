"""Decoding register codes to words: a code the table lacks gives ``None``, never the raw code."""

from vestagraph_area.energy_certificate import decode


def test_decode_known_code_words() -> None:
    assert decode(2, {0: "House", 2: "Flat"}) == "Flat"


def test_decode_unknown_code_none() -> None:
    assert decode(99, {0: "House", 2: "Flat"}) is None
