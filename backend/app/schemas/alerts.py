from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.scoring import RiskLevel

AlertStatus = Literal[
    "OPEN",
    "UNDER_REVIEW",
    "RESOLVED",
    "CLOSED",
]


class AlertResponse(BaseModel):
    """API representation of a fraud investigation alert."""

    model_config = ConfigDict(extra="forbid")

    alert_id: str = Field(min_length=1, max_length=128)
    transaction_id: str = Field(min_length=1, max_length=128)

    risk_score: float = Field(ge=0.0, le=1.0)
    risk_level: RiskLevel

    rule_signals: list[str] = Field(default_factory=list)

    model_probability: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    feature_evidence: dict[str, float | str | bool | None] = Field(default_factory=dict)

    created_at: datetime
    status: AlertStatus = "OPEN"

    model_version: str | None = None


AnalystDecision = Literal["APPROVE", "FLAG", "LEGITIMATE"]


class AnalystDecisionRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    decision: AnalystDecision
    analyst_id: str = Field(
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$",
    )
    rationale: str | None = Field(
        default=None,
        max_length=2000,
    )
