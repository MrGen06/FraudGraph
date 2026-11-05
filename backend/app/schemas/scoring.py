from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

RiskLevel = Literal["LOW", "MEDIUM", "HIGH"]


class RiskScoreResponse(BaseModel):
    """Explainable operational fraud risk assessment."""

    model_config = ConfigDict(extra="forbid")

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

    model_version: str | None = None
