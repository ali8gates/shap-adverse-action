"""Ties the pieces together: score, direction, reasons, contracts, letter.

This is the shape the real system follows: a decision does not become a
customer letter until it has passed the data contract checks and the
reason quality gate. Anything that fails either one gets held for a human
to look at instead of going out the door incomplete or wrong.
"""

from dataclasses import dataclass, field

from .data_contracts import check_fully_null, run_contract_checks
from .direction import direct_all
from .models import Applicant, Outcome
from .reason_selection import select_top_positive_reasons
from .templates import FEATURE_TO_REASON_CODE, INSUFFICIENT_INFORMATION_CODE, reason_codes_from_shap, render_reasons

DECLINE_SCORE_THRESHOLD = 0.65
LINE_DECREASE_SCORE_THRESHOLD = 0.45


@dataclass(frozen=True)
class DecisionResult:
    applicant_id: str
    outcome: Outcome
    reason_codes: list[str] = field(default_factory=list)
    reason_text: list[str] = field(default_factory=list)
    contract_problems: list[str] = field(default_factory=list)
    held_for_review: bool = False


def _score_outcome(score: float) -> Outcome:
    if score >= DECLINE_SCORE_THRESHOLD:
        return Outcome.DECLINED
    if score >= LINE_DECREASE_SCORE_THRESHOLD:
        return Outcome.LINE_DECREASE
    return Outcome.APPROVED


def decide(applicant: Applicant) -> DecisionResult:
    contract = run_contract_checks(applicant.features)

    if check_fully_null(applicant.features):
        codes = [INSUFFICIENT_INFORMATION_CODE]
        return DecisionResult(
            applicant_id=applicant.applicant_id,
            outcome=Outcome.DECLINED,
            reason_codes=codes,
            reason_text=render_reasons(codes),
            contract_problems=contract.problems,
        )

    outcome = _score_outcome(applicant.model_score)

    if outcome is Outcome.APPROVED:
        return DecisionResult(applicant_id=applicant.applicant_id, outcome=outcome, contract_problems=contract.problems)

    directed = direct_all(applicant.shap_values)
    top_reasons = select_top_positive_reasons(directed)
    codes = reason_codes_from_shap(top_reasons, FEATURE_TO_REASON_CODE)
    text = render_reasons(codes)

    return DecisionResult(
        applicant_id=applicant.applicant_id,
        outcome=outcome,
        reason_codes=codes,
        reason_text=text,
        contract_problems=contract.problems,
        held_for_review=not contract.passed,
    )
