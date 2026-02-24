"""Turning selected SHAP reasons into the text that goes in a letter.

Two pipeline bugs showed up after the SHAP math was already correct.
First, some reason codes existed in the model output but had no matching
text in the template table, which produced blank or half filled letters.
Second, when a decision had more than one reason, the template step
sometimes rendered only the first one and quietly dropped the rest.

The quality gate here exists to make both of those impossible: every
reason code either has approved text or the letter fails loudly instead of
going out incomplete, and rendering always walks the full reason list.
"""

from dataclasses import dataclass

from .reason_selection import AdverseActionReason

INSUFFICIENT_INFORMATION_CODE = "insufficient_information"

REASON_CODE_TEXT: dict[str, str] = {
    "low_account_tenure": "Length of banking relationship is too short to establish a reliable pattern.",
    "low_inflow_stability": "Income deposits are irregular or inconsistent over the review period.",
    "high_recent_loan_activity": "A high number of recent loan payments relative to account history.",
    "low_debit_transaction_count": "Low number of debit transactions over the review period.",
    "high_overdraft_frequency": "Frequent overdrafts within the review period.",
    "low_balance_buffer": "Account balance stays close to zero for extended periods.",
    "thin_cash_flow_history": "Limited cash flow history available for review.",
    "high_credit_utilization": "Credit utilization is high relative to available limits.",
    INSUFFICIENT_INFORMATION_CODE: "There is not enough account history available to generate a decision.",
}


FEATURE_TO_REASON_CODE: dict[str, str] = {
    "account_tenure_days": "low_account_tenure",
    "inflow_stability_score": "low_inflow_stability",
    "recent_loan_payment_count": "high_recent_loan_activity",
    "debit_transaction_count": "low_debit_transaction_count",
    "overdraft_count": "high_overdraft_frequency",
    "average_balance_buffer": "low_balance_buffer",
    "cash_flow_history_days": "thin_cash_flow_history",
    "credit_utilization_ratio": "high_credit_utilization",
}


@dataclass(frozen=True)
class QualityGateResult:
    passed: bool
    unmapped_codes: list[str]


def run_quality_gate(reason_codes: list[str]) -> QualityGateResult:
    """Confirms every reason code about to go on a letter has approved text.

    A reason with no mapped text should stop the letter, not go out blank.
    """

    unmapped = [code for code in reason_codes if code not in REASON_CODE_TEXT]
    return QualityGateResult(passed=len(unmapped) == 0, unmapped_codes=unmapped)


def render_reasons(reason_codes: list[str]) -> list[str]:
    """Renders the full list of reason codes to text, in order.

    This always iterates the entire list. The earlier bug that rendered
    only the first reason in a multi-reason letter came from a call site
    that indexed into the list instead of looping over it.
    """

    gate = run_quality_gate(reason_codes)
    if not gate.passed:
        raise ValueError(f"Reason codes missing template text: {gate.unmapped_codes}")
    return [REASON_CODE_TEXT[code] for code in reason_codes]


def reason_codes_from_shap(reasons: list[AdverseActionReason], feature_to_code: dict[str, str]) -> list[str]:
    return [feature_to_code[r.feature] for r in reasons if r.feature in feature_to_code]
