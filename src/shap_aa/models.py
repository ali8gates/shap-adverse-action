"""Data shapes for one lending decision and its SHAP explanation.

A decision carries a score and a set of per-feature SHAP values for one
applicant. Everything downstream, direction, reason selection, and the
customer letter, is derived from this, not recomputed from scratch.
"""

from dataclasses import dataclass
from enum import Enum


class Product(Enum):
    VA_DAY_ZERO = "va_day_zero"
    VA_CLASSIC = "va_classic"


class FeedSource(Enum):
    """Which Plaid feed a feature was built from.

    CRA and non-CRA feeds can categorize the same transaction differently
    and use different lookback windows, so a feature is only comparable to
    another feature built from the same feed.
    """

    CRA_BASELINE = "cra_baseline"
    CRA_CASH_FLOW = "cra_cash_flow"
    NON_CRA = "non_cra"


@dataclass(frozen=True)
class FeatureValue:
    name: str
    value: float | None
    feed: FeedSource
    lookback_days: int


@dataclass(frozen=True)
class ShapAttribution:
    """One feature's SHAP contribution for one applicant's decision.

    A positive value means the feature pushed risk up for this specific
    applicant. A negative value means it pushed risk down. This is always
    read per record, never as a dataset-wide average, see direction.py for
    why that distinction is the whole point of this repo.
    """

    feature: str
    shap_value: float


@dataclass(frozen=True)
class Applicant:
    applicant_id: str
    product: Product
    features: tuple[FeatureValue, ...]
    shap_values: tuple[ShapAttribution, ...]
    model_score: float


class Outcome(Enum):
    APPROVED = "approved"
    DECLINED = "declined"
    LINE_DECREASE = "line_decrease"
