from shap_aa.models import Outcome
from shap_aa.pipeline import decide
from shap_aa.sample_data import SAMPLE_APPLICANTS


def _find(applicant_id):
    return next(a for a in SAMPLE_APPLICANTS if a.applicant_id == applicant_id)


def test_decline_gets_up_to_four_reasons():
    result = decide(_find("APP-1001"))
    assert result.outcome is Outcome.DECLINED
    assert 1 <= len(result.reason_codes) <= 4
    assert len(result.reason_text) == len(result.reason_codes)


def test_line_decrease_with_two_available_reasons():
    result = decide(_find("APP-1002"))
    assert result.outcome is Outcome.LINE_DECREASE
    assert len(result.reason_codes) == 2


def test_approval_has_no_adverse_action_reasons():
    result = decide(_find("APP-1003"))
    assert result.outcome is Outcome.APPROVED
    assert result.reason_codes == []


def test_fully_null_features_route_to_insufficient_information():
    result = decide(_find("APP-1004"))
    assert result.outcome is Outcome.DECLINED
    assert result.reason_codes == ["insufficient_information"]


def test_lookback_mismatch_holds_the_letter_for_review():
    result = decide(_find("APP-1005"))
    assert result.contract_problems
    assert result.held_for_review is True


def test_every_processed_applicant_gets_a_result():
    for applicant in SAMPLE_APPLICANTS:
        result = decide(applicant)
        assert result.applicant_id == applicant.applicant_id
