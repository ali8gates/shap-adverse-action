"""Choosing which SHAP values become adverse action reasons.

The first version ranked features by absolute SHAP magnitude, which is a
fine way to debug a model and a bad way to write a denial letter. A large
negative SHAP value means a feature made the applicant look better, and
ranking by magnitude alone can put that feature in the top four reasons
for a decline. Read literally, that produces a reason that argues against
the decision it is attached to.

Adverse action reasons should answer one question only: why did risk come
out too high. That means selecting from positive SHAP values, the ones
that pushed risk up, and ignoring negative SHAP values for this purpose
even when they are large. Negative SHAP values are not thrown away, they
stay in the score log and the monitoring views, they just never become a
customer-facing reason.
"""

from dataclasses import dataclass

from .direction import Direction, DirectedAttribution

MAX_REASONS = 4


@dataclass(frozen=True)
class AdverseActionReason:
    feature: str
    shap_value: float
    rank: int


def select_top_positive_reasons(directed: list[DirectedAttribution], max_reasons: int = MAX_REASONS) -> list[AdverseActionReason]:
    """Ranks only the risk-increasing SHAP values and keeps the top N.

    Risk-decreasing values are excluded entirely here, on purpose. They
    belong in model monitoring, not in a denial letter.
    """

    risk_increasing = [d for d in directed if d.direction is Direction.INCREASES_RISK]
    ranked = sorted(risk_increasing, key=lambda d: d.shap_value, reverse=True)
    top = ranked[:max_reasons]
    return [AdverseActionReason(feature=d.feature, shap_value=d.shap_value, rank=i + 1) for i, d in enumerate(top)]


def select_top_absolute_reasons(directed: list[DirectedAttribution], max_reasons: int = MAX_REASONS) -> list[AdverseActionReason]:
    """The old approach, ranking by absolute SHAP magnitude regardless of
    direction. Kept only so tests can demonstrate why it was replaced.
    """

    ranked = sorted(directed, key=lambda d: abs(d.shap_value), reverse=True)
    top = ranked[:max_reasons]
    return [AdverseActionReason(feature=d.feature, shap_value=d.shap_value, rank=i + 1) for i, d in enumerate(top)]
