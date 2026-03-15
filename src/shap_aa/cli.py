"""Command line entry point for the SHAP adverse action demo.

Run it with:

    python -m shap_aa.cli

Everything it processes is synthetic sample data. See sample_data.py.
"""

from .backfill import BackfillRecord, compare_backfill
from .models import Outcome
from .pipeline import decide
from .sample_data import SAMPLE_APPLICANTS

DIVIDER = "-" * 78


def _print_decision(result) -> None:
    tag = {
        Outcome.APPROVED: "APPROVED    ",
        Outcome.DECLINED: "DECLINED    ",
        Outcome.LINE_DECREASE: "LINE DECREASE",
    }[result.outcome]
    print(f"[{tag}] {result.applicant_id}")
    if result.reason_text:
        for i, text in enumerate(result.reason_text, start=1):
            print(f"    reason {i}: {text}")
    else:
        print("    no adverse action reasons needed")
    if result.contract_problems:
        print(f"    data contract problem: {'; '.join(result.contract_problems)}")
    if result.held_for_review:
        print("    held for review before this letter goes out")
    print()


def main() -> None:
    print(DIVIDER)
    print("SHAP driven adverse action, demo run on synthetic applicants")
    print(DIVIDER)
    print()

    results = [decide(a) for a in SAMPLE_APPLICANTS]
    for result in results:
        _print_decision(result)

    declined_or_reduced = [r for r in results if r.outcome is not Outcome.APPROVED]
    held = [r for r in results if r.held_for_review]

    print(DIVIDER)
    print("Batch summary")
    print(DIVIDER)
    print(f"Applicants processed:         {len(results)}")
    print(f"Declined or line decreased:   {len(declined_or_reduced)}")
    print(f"Held for review before send:  {len(held)}")
    print()

    print(DIVIDER)
    print("Shadow scoring vs backfill, one matched batch and one mismatch")
    print(DIVIDER)
    live = [
        BackfillRecord("APP-1001", {"account_tenure_days": 40.0}, 0.81, ["low_account_tenure", "high_recent_loan_activity"]),
        BackfillRecord("APP-1002", {"inflow_stability_score": 0.3}, 0.52, ["low_inflow_stability"]),
    ]
    backfilled_clean = [
        BackfillRecord("APP-1001", {"account_tenure_days": 40.0}, 0.81, ["low_account_tenure", "high_recent_loan_activity"]),
        BackfillRecord("APP-1002", {"inflow_stability_score": 0.3}, 0.52, ["low_inflow_stability"]),
    ]
    clean_report = compare_backfill(live, backfilled_clean)
    print(f"Clean backfill match rate: {clean_report.match_rate:.0%} ({clean_report.matched}/{clean_report.total})")

    backfilled_drifted = [
        BackfillRecord("APP-1001", {"account_tenure_days": 40.0}, 0.81, ["low_account_tenure", "high_recent_loan_activity"]),
        BackfillRecord("APP-1002", {"inflow_stability_score": 0.3}, 0.60, ["low_inflow_stability"]),
    ]
    drifted_report = compare_backfill(live, backfilled_drifted)
    print(f"Drifted backfill match rate: {drifted_report.match_rate:.0%} ({drifted_report.matched}/{drifted_report.total})")
    for problem in drifted_report.mismatches:
        print(f"    mismatch: {problem}")
    print()

    print("This is the shape of the real validation: run shadow scoring on live")
    print("traffic, backfill historical cohorts, and require a full match on")
    print("feature values, model scores, and reason codes before anything about")
    print("adverse action changes for a real customer.")


if __name__ == "__main__":
    main()
