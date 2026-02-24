"""Synthetic applicants covering every path in the pipeline.

Nothing here is a real customer, a real feature value, or a real SHAP
output. The scenarios are chosen to hit the same set of cases that showed
up in review during the real build: a clean decline with a full reason
set, a line decrease with fewer than four available reasons, an approval
that needs no adverse action reasons at all, a fully null feature set, and
a decline where the underlying data has a contract problem that should
hold the letter for a human.
"""

from .models import Applicant, FeatureValue, FeedSource, Product, ShapAttribution

SAMPLE_APPLICANTS = [
    Applicant(
        applicant_id="APP-1001",
        product=Product.VA_CLASSIC,
        features=(
            FeatureValue("account_tenure_days", 40, FeedSource.NON_CRA, 125),
            FeatureValue("recent_loan_payment_count", 6, FeedSource.CRA_CASH_FLOW, 180),
            FeatureValue("overdraft_count", 5, FeedSource.CRA_CASH_FLOW, 180),
            FeatureValue("average_balance_buffer", 12.0, FeedSource.CRA_BASELINE, 180),
            FeatureValue("debit_transaction_count", 3, FeedSource.NON_CRA, 125),
        ),
        shap_values=(
            ShapAttribution("account_tenure_days", 0.21),
            ShapAttribution("recent_loan_payment_count", 0.18),
            ShapAttribution("overdraft_count", 0.14),
            ShapAttribution("average_balance_buffer", 0.09),
            ShapAttribution("debit_transaction_count", 0.05),
            ShapAttribution("credit_utilization_ratio", -0.11),
        ),
        model_score=0.81,
    ),
    Applicant(
        applicant_id="APP-1002",
        product=Product.VA_DAY_ZERO,
        features=(
            FeatureValue("inflow_stability_score", 0.3, FeedSource.NON_CRA, 125),
            FeatureValue("cash_flow_history_days", 60, FeedSource.CRA_CASH_FLOW, 180),
            FeatureValue("average_balance_buffer", 15.0, FeedSource.CRA_BASELINE, 180),
        ),
        shap_values=(
            ShapAttribution("inflow_stability_score", 0.16),
            ShapAttribution("cash_flow_history_days", 0.07),
            ShapAttribution("account_tenure_days", -0.22),
        ),
        model_score=0.52,
    ),
    Applicant(
        applicant_id="APP-1003",
        product=Product.VA_CLASSIC,
        features=(
            FeatureValue("account_tenure_days", 720, FeedSource.NON_CRA, 125),
            FeatureValue("credit_utilization_ratio", 0.12, FeedSource.CRA_BASELINE, 180),
            FeatureValue("recent_loan_payment_count", 1, FeedSource.CRA_CASH_FLOW, 180),
        ),
        shap_values=(
            ShapAttribution("account_tenure_days", -0.30),
            ShapAttribution("credit_utilization_ratio", -0.05),
            ShapAttribution("overdraft_count", 0.02),
        ),
        model_score=0.11,
    ),
    Applicant(
        applicant_id="APP-1004",
        product=Product.VA_DAY_ZERO,
        features=(
            FeatureValue("account_tenure_days", None, FeedSource.NON_CRA, 125),
            FeatureValue("inflow_stability_score", None, FeedSource.NON_CRA, 125),
            FeatureValue("cash_flow_history_days", None, FeedSource.CRA_CASH_FLOW, 180),
            FeatureValue("average_balance_buffer", None, FeedSource.CRA_BASELINE, 180),
        ),
        shap_values=(),
        model_score=0.0,
    ),
    Applicant(
        applicant_id="APP-1005",
        product=Product.VA_CLASSIC,
        features=(
            FeatureValue("recent_loan_payment_count", 4, FeedSource.CRA_CASH_FLOW, 125),
            FeatureValue("average_balance_buffer", 8.0, FeedSource.CRA_BASELINE, 180),
        ),
        shap_values=(
            ShapAttribution("recent_loan_payment_count", 0.24),
            ShapAttribution("average_balance_buffer", 0.10),
        ),
        model_score=0.70,
    ),
]
