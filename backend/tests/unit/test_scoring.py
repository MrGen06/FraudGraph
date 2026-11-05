import pytest
from pydantic import ValidationError

from app.schemas.scoring import RiskScoreResponse


def valid_risk_score() -> dict:
    return {
        "transaction_id": "TX001",
        "risk_score": 0.85,
        "risk_level": "HIGH",
        "rule_signals": ["HIGH_FAN_IN", "SHARED_DEVICE"],
        "model_probability": 0.92,
        "feature_evidence": {
            "fan_in_count": 8.0,
            "shared_device": True,
        },
        "model_version": "baseline-v1",
    }


def test_valid_risk_score_is_accepted() -> None:
    result = RiskScoreResponse(**valid_risk_score())

    assert result.transaction_id == "TX001"
    assert result.risk_score == 0.85
    assert result.risk_level == "HIGH"


@pytest.mark.parametrize("score", [-0.1, 1.1])
def test_risk_score_out_of_range_is_rejected(score: float) -> None:
    data = valid_risk_score()
    data["risk_score"] = score

    with pytest.raises(ValidationError):
        RiskScoreResponse(**data)


@pytest.mark.parametrize("probability", [-0.1, 1.1])
def test_model_probability_out_of_range_is_rejected(
    probability: float,
) -> None:
    data = valid_risk_score()
    data["model_probability"] = probability

    with pytest.raises(ValidationError):
        RiskScoreResponse(**data)


def test_model_probability_can_be_none() -> None:
    data = valid_risk_score()
    data["model_probability"] = None

    result = RiskScoreResponse(**data)

    assert result.model_probability is None


def test_invalid_risk_level_is_rejected() -> None:
    data = valid_risk_score()
    data["risk_level"] = "CRITICAL"

    with pytest.raises(ValidationError):
        RiskScoreResponse(**data)


def test_unknown_field_is_rejected() -> None:
    data = valid_risk_score()
    data["unexpected_field"] = "invalid"

    with pytest.raises(ValidationError):
        RiskScoreResponse(**data)
