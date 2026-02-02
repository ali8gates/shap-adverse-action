"""Checks that catch CRA and non-CRA data problems before scoring.

Adverse action reasons have to be grounded in the same feed that was
certified for credit decisions. Two problems kept showing up here:

  - CRA and non-CRA transaction feeds sometimes categorize the same
    transaction differently (rent counted as a loan payment, for example),
    which silently changes a feature's value depending on which feed built
    it.
  - CRA and non-CRA pulls used different lookback windows, so the same
    applicant could have a different effective feature set depending on
    which feed you asked.
  - CRA data arrives as two separate segments, baseline and cash flow, and
    a feature set is incomplete if only one of the two came back.

None of this is something a model can catch on its own. These are gate
checks that run before a decision is scored, so a bad or partial feed
never quietly turns into a wrong reason on a customer letter.
"""

from dataclasses import dataclass, field

from .models import FeatureValue, FeedSource

EXPECTED_LOOKBACK_DAYS = {
    FeedSource.CRA_BASELINE: 180,
    FeedSource.CRA_CASH_FLOW: 180,
    FeedSource.NON_CRA: 125,
}


@dataclass(frozen=True)
class ContractCheckResult:
    passed: bool
    problems: list[str] = field(default_factory=list)


def check_lookback_windows(features: tuple[FeatureValue, ...]) -> list[str]:
    problems = []
    for f in features:
        expected = EXPECTED_LOOKBACK_DAYS.get(f.feed)
        if expected is not None and f.lookback_days != expected:
            problems.append(
                f"{f.name}: built on a {f.lookback_days} day window, expected {expected} for {f.feed.value}"
            )
    return problems


def check_cra_segments_present(features: tuple[FeatureValue, ...]) -> list[str]:
    feeds_present = {f.feed for f in features}
    problems = []
    has_any_cra = FeedSource.CRA_BASELINE in feeds_present or FeedSource.CRA_CASH_FLOW in feeds_present
    if has_any_cra:
        if FeedSource.CRA_BASELINE not in feeds_present:
            problems.append("CRA cash flow segment present without the CRA baseline segment")
        if FeedSource.CRA_CASH_FLOW not in feeds_present:
            problems.append("CRA baseline segment present without the CRA cash flow segment")
    return problems


def check_fully_null(features: tuple[FeatureValue, ...]) -> bool:
    """True when every feature in the lookback window came back empty.

    This is not a contract failure, it is a real state an applicant can be
    in, and it needs its own path rather than falling through the normal
    scoring and reason logic silently.
    """

    return len(features) > 0 and all(f.value is None for f in features)


def run_contract_checks(features: tuple[FeatureValue, ...]) -> ContractCheckResult:
    problems = check_lookback_windows(features) + check_cra_segments_present(features)
    return ContractCheckResult(passed=len(problems) == 0, problems=problems)
