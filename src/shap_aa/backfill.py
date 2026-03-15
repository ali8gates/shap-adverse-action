"""Comparing a live decision against a backfilled one.

Before any of this reached customers, we ran it in shadow mode against
live traffic and backfilled it against historical cohorts, then compared
feature values, model scores, and reason codes between the two runs. A
match here means the model math and the letter a customer would have
received agree with each other. A mismatch means something upstream, a
feed, a window, a mapping, moved between the two runs and needs a human
before anything ships.
"""

from dataclasses import dataclass, field

FLOAT_TOLERANCE = 1e-6


@dataclass(frozen=True)
class BackfillRecord:
    applicant_id: str
    feature_values: dict[str, float | None]
    model_score: float
    reason_codes: list[str]


@dataclass(frozen=True)
class MatchReport:
    total: int
    matched: int
    mismatches: list[str] = field(default_factory=list)

    @property
    def fully_matched(self) -> bool:
        return self.total > 0 and self.matched == self.total

    @property
    def match_rate(self) -> float:
        return self.matched / self.total if self.total else 0.0


def _records_match(live: BackfillRecord, backfilled: BackfillRecord) -> str | None:
    if live.feature_values != backfilled.feature_values:
        return f"{live.applicant_id}: feature values differ between live and backfill"
    if abs(live.model_score - backfilled.model_score) > FLOAT_TOLERANCE:
        return f"{live.applicant_id}: model score differs, live={live.model_score} backfill={backfilled.model_score}"
    if live.reason_codes != backfilled.reason_codes:
        return f"{live.applicant_id}: reason codes differ, live={live.reason_codes} backfill={backfilled.reason_codes}"
    return None


def compare_backfill(live: list[BackfillRecord], backfilled: list[BackfillRecord]) -> MatchReport:
    backfilled_by_id = {r.applicant_id: r for r in backfilled}
    mismatches = []
    matched = 0

    for live_record in live:
        counterpart = backfilled_by_id.get(live_record.applicant_id)
        if counterpart is None:
            mismatches.append(f"{live_record.applicant_id}: no matching backfill record")
            continue
        problem = _records_match(live_record, counterpart)
        if problem:
            mismatches.append(problem)
        else:
            matched += 1

    return MatchReport(total=len(live), matched=matched, mismatches=mismatches)
