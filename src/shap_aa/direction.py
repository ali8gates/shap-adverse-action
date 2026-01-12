"""Per-record SHAP direction, and the batch-mean bug it replaced.

The first version of this system decided whether a feature "increases risk"
or "decreases risk" by looking at that feature's mean SHAP value across a
batch or a whole dataset. That is a reasonable question to ask about a
model in general, and a wrong question to ask about one customer's letter.

A feature can have a positive mean SHAP across a portfolio and still carry
a negative SHAP value for a specific applicant. Under the batch-mean rule,
that applicant could see a reason like "recent loan activity increased
your risk" on a decision where that exact feature was actually pulling
their risk down. The fix is not a smarter model, it is asking the
direction question at the right level: one applicant, one decision, one
signed SHAP value at a time.
"""

from dataclasses import dataclass
from enum import Enum

from .models import ShapAttribution


class Direction(Enum):
    INCREASES_RISK = "increases_risk"
    DECREASES_RISK = "decreases_risk"


@dataclass(frozen=True)
class DirectedAttribution:
    feature: str
    shap_value: float
    direction: Direction


def batch_mean_direction(feature: str, shap_values_across_batch: list[float]) -> Direction:
    """The old approach: one direction label per feature, from the batch
    mean. Kept here only so the tests can show exactly where it disagrees
    with the per-record version below.
    """

    mean_value = sum(shap_values_across_batch) / len(shap_values_across_batch)
    return Direction.INCREASES_RISK if mean_value > 0 else Direction.DECREASES_RISK


def per_record_direction(attribution: ShapAttribution) -> DirectedAttribution:
    """The corrected approach: direction comes from this applicant's own
    signed SHAP value for this feature, never from a batch average.
    """

    direction = Direction.INCREASES_RISK if attribution.shap_value > 0 else Direction.DECREASES_RISK
    return DirectedAttribution(feature=attribution.feature, shap_value=attribution.shap_value, direction=direction)


def direct_all(shap_values: tuple[ShapAttribution, ...]) -> list[DirectedAttribution]:
    return [per_record_direction(a) for a in shap_values]
