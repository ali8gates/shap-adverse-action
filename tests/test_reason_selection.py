from shap_aa.direction import direct_all
from shap_aa.models import ShapAttribution
from shap_aa.reason_selection import select_top_absolute_reasons, select_top_positive_reasons


def test_positive_only_selection_excludes_a_large_negative_shap():
    shap_values = (
        ShapAttribution("recent_loan_payment_count", 0.30),
        ShapAttribution("account_tenure_days", -0.90),  # large, but risk-reducing
        ShapAttribution("overdraft_count", 0.10),
    )
    directed = direct_all(shap_values)
    reasons = select_top_positive_reasons(directed)
    feature_names = [r.feature for r in reasons]
    assert "account_tenure_days" not in feature_names


def test_absolute_selection_would_have_included_the_large_negative_shap():
    shap_values = (
        ShapAttribution("recent_loan_payment_count", 0.30),
        ShapAttribution("account_tenure_days", -0.90),
        ShapAttribution("overdraft_count", 0.10),
    )
    directed = direct_all(shap_values)
    reasons = select_top_absolute_reasons(directed, max_reasons=1)
    assert reasons[0].feature == "account_tenure_days"


def test_selection_caps_at_four_reasons():
    shap_values = tuple(ShapAttribution(f"feature_{i}", 0.1 * (i + 1)) for i in range(6))
    directed = direct_all(shap_values)
    reasons = select_top_positive_reasons(directed)
    assert len(reasons) == 4


def test_ranks_are_ordered_highest_shap_first():
    shap_values = (
        ShapAttribution("a", 0.10),
        ShapAttribution("b", 0.40),
        ShapAttribution("c", 0.25),
    )
    directed = direct_all(shap_values)
    reasons = select_top_positive_reasons(directed)
    assert [r.feature for r in reasons] == ["b", "c", "a"]
    assert [r.rank for r in reasons] == [1, 2, 3]
