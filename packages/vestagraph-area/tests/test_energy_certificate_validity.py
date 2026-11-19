"""Energy certificate validity: ten years from the date it was entered on the register.

Source (checked 18 Nov 2026): the Energy Performance of Buildings (England and
Wales) Regulations 2012, regulation 9(2)(a), at
https://www.legislation.gov.uk/uksi/2012/3118/regulation/9 : a certificate is
valid only if "it was entered on the register no more than 10 years before the
date on which it is made available". So the 10 years run from the REGISTRATION
date (not inspection or issue), and the last valid day is the same day and
month 10 years on. GOV.UK's guide
(https://www.gov.uk/government/publications/energy-performance-certificates-for-the-construction-sale-and-let-of-dwellings/a-guide-to-energy-performance-certificates-for-the-marketing-sale-and-let-of-dwellings)
says "valid for 10 years" and is silent on the start date and on 29 February.
The Find an energy certificate page states no "valid until" rule, so the
service's own display could not be confirmed.

29 February is the agent's call, checked against regulation 9(2)(a): registered
on 2016-02-29, the certificate is no more than 10 years old on 2026-02-28
(10 years before that is 2016-02-28, earlier than the registration), and more
than 10 years old on 2026-03-01 (10 years before is 2016-03-01, later than the
registration). So its last valid day is 28 February.

Regulation 9(2)(b) adds a second limb: a certificate is only valid if "no other energy
performance certificate for the building has since been entered on the register" (checked
19 Nov 2026). That limb depends on the register's status, not on dates, so these functions
cover limb (a) only; the generator writes a validity date only for a current ("entered")
certificate. The regulation is silent on a cancelled certificate, which also shows no date.
"""

from datetime import date

from vestagraph_area.energy_certificate import is_more_than_ten_years_old, valid_until


def test_valid_until_ordinary_date_adds_ten_years() -> None:
    # Working: 2025 + 10 = 2035; month and day unchanged.
    assert valid_until(date(2025, 4, 4)) == date(2035, 4, 4)


def test_valid_until_leap_day_gives_28_february() -> None:
    # Working: 2026 is not a leap year, so 29 Feb does not exist; see docstring.
    assert valid_until(date(2016, 2, 29)) == date(2026, 2, 28)


def test_is_more_than_ten_years_old_on_the_last_valid_day_false() -> None:
    # Working: 2016-10-23 + 10 years = 2026-10-23, "no more than 10 years" holds.
    assert not is_more_than_ten_years_old(date(2016, 10, 23), date(2026, 10, 23))


def test_is_more_than_ten_years_old_day_after_true() -> None:
    # Working: 2016-10-22 + 10 years = 2026-10-22; 2026-10-23 is one day later.
    assert is_more_than_ten_years_old(date(2016, 10, 22), date(2026, 10, 23))


def test_is_more_than_ten_years_old_leap_day_start_on_28_february_false() -> None:
    # Working: last valid day for a 29 Feb 2016 start is 2026-02-28.
    assert not is_more_than_ten_years_old(date(2016, 2, 29), date(2026, 2, 28))


def test_is_more_than_ten_years_old_leap_day_start_on_1_march_true() -> None:
    # Working: 10 years before 2026-03-01 is 2016-03-01, after the 2016-02-29 registration.
    assert is_more_than_ten_years_old(date(2016, 2, 29), date(2026, 3, 1))
