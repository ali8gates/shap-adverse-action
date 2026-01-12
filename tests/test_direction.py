from shap_aa.direction import Direction, batch_mean_direction, per_record_direction
from shap_aa.models import ShapAttribution


def test_batch_mean_can_disagree_with_an_individual_record():
    # A feature with a positive mean across the batch, but this particular
    # applicant's own SHAP value for it is negative.
    batch_values = [0.30, 0.25, -0.05, 0.10]
    batch_direction = batch_mean_direction("recent_loan_payment_count", batch_values)
    assert batch_direction is Direction.INCREASES_RISK

    this_applicant = ShapAttribution("recent_loan_payment_count", -0.05)
    record_direction = per_record_direction(this_applicant)
    assert record_direction.direction is Direction.DECREASES_RISK

    # This is exactly the mismatch that made the old labeling wrong.
    assert batch_direction is not record_direction.direction


def test_positive_shap_is_always_increases_risk_per_record():
    attribution = ShapAttribution("overdraft_count", 0.01)
    result = per_record_direction(attribution)
    assert result.direction is Direction.INCREASES_RISK


def test_negative_shap_is_always_decreases_risk_per_record():
    attribution = ShapAttribution("account_tenure_days", -0.01)
    result = per_record_direction(attribution)
    assert result.direction is Direction.DECREASES_RISK
