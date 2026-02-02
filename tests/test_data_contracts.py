from shap_aa.data_contracts import check_cra_segments_present, check_fully_null, run_contract_checks
from shap_aa.models import FeatureValue, FeedSource


def test_mismatched_lookback_window_is_flagged():
    features = (
        FeatureValue("recent_loan_payment_count", 4, FeedSource.CRA_CASH_FLOW, 125),
        FeatureValue("average_balance_buffer", 10.0, FeedSource.CRA_BASELINE, 180),
    )
    result = run_contract_checks(features)
    assert not result.passed
    assert any("180" in p for p in result.problems)


def test_matching_lookback_window_passes():
    features = (
        FeatureValue("recent_loan_payment_count", 4, FeedSource.CRA_CASH_FLOW, 180),
        FeatureValue("average_balance_buffer", 10.0, FeedSource.CRA_BASELINE, 180),
    )
    result = run_contract_checks(features)
    assert result.passed


def test_cra_baseline_without_cash_flow_is_flagged():
    features = (FeatureValue("average_balance_buffer", 10.0, FeedSource.CRA_BASELINE, 180),)
    problems = check_cra_segments_present(features)
    assert len(problems) == 1
    assert "cash flow" in problems[0]


def test_both_cra_segments_present_is_clean():
    features = (
        FeatureValue("average_balance_buffer", 10.0, FeedSource.CRA_BASELINE, 180),
        FeatureValue("recent_loan_payment_count", 4, FeedSource.CRA_CASH_FLOW, 180),
    )
    assert check_cra_segments_present(features) == []


def test_fully_null_feature_set_is_detected():
    features = (
        FeatureValue("account_tenure_days", None, FeedSource.NON_CRA, 125),
        FeatureValue("inflow_stability_score", None, FeedSource.NON_CRA, 125),
    )
    assert check_fully_null(features) is True


def test_partially_null_feature_set_is_not_fully_null():
    features = (
        FeatureValue("account_tenure_days", 40, FeedSource.NON_CRA, 125),
        FeatureValue("inflow_stability_score", None, FeedSource.NON_CRA, 125),
    )
    assert check_fully_null(features) is False
