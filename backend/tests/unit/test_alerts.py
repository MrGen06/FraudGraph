from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.schemas.alerts import (
    AlertResponse,
    AnalystDecisionRequest,
)


def valid_alert() -> dict:
    return {
        "alert_id": "ALERT001",
        "transaction_id": "TX001",
        "risk_score": 0.85,
        "risk_level": "HIGH",
        "rule_signals": ["HIGH_FAN_IN"],
        "model_probability": None,
        "feature_evidence": {"fan_in_count": 8.0},
        "created_at": datetime.now(UTC),
        "status": "OPEN",
        "model_version": None,
    }


def test_valid_alert_is_accepted() -> None:
    alert = AlertResponse(**valid_alert())

    assert alert.alert_id == "ALERT001"
    assert alert.risk_level == "HIGH"
    assert alert.status == "OPEN"


@pytest.mark.parametrize(
    "status",
    ["OPEN", "UNDER_REVIEW", "RESOLVED", "CLOSED"],
)
def test_valid_alert_statuses(status: str) -> None:
    data = valid_alert()
    data["status"] = status

    alert = AlertResponse(**data)

    assert alert.status == status


def test_invalid_alert_status_is_rejected() -> None:
    data = valid_alert()
    data["status"] = "PENDING"

    with pytest.raises(ValidationError):
        AlertResponse(**data)


@pytest.mark.parametrize(
    "decision",
    ["APPROVE", "FLAG", "LEGITIMATE"],
)
def test_valid_analyst_decisions(decision: str) -> None:
    request = AnalystDecisionRequest.model_validate(
        {
            "decision": decision,
            "analyst_id": "DEMO-ANALYST",
        }
    )
    assert request.decision == decision


def test_analyst_rationale_is_optional() -> None:
    request = AnalystDecisionRequest(
        decision="FLAG",
        analyst_id="DEMO-ANALYST",
    )

    assert request.rationale is None


def test_empty_analyst_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        AnalystDecisionRequest(
            decision="FLAG",
            analyst_id="",
        )


def test_invalid_analyst_decision_is_rejected() -> None:
    with pytest.raises(ValidationError):
        AnalystDecisionRequest.model_validate(
            {
                "decision": "MAYBE",
                "analyst_id": "DEMO-ANALYST",
            }
        )
