from datetime import UTC, datetime
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

Identifier = Annotated[
    str,
    Field(
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$",
    ),
]


class TransactionLocation(BaseModel):
    """Geographic information associated with a transaction."""

    model_config = ConfigDict(extra="forbid")

    country: str | None = Field(default=None, min_length=2, max_length=2)
    region: str | None = Field(default=None, min_length=1, max_length=64)

    @field_validator("country")
    @classmethod
    def normalize_country(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.upper()


class NormalizedTransaction(BaseModel):
    """Canonical transaction event used throughout FraudGraph."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    transaction_id: Identifier
    timestamp: datetime

    source_account_id: Identifier
    destination_account_id: Identifier | None = None

    user_id: Identifier | None = None
    card_id: Identifier | None = None
    device_id: Identifier | None = None
    ip_id: Identifier | None = None
    merchant_id: Identifier | None = None

    amount: float = Field(gt=0)
    currency: str = Field(pattern=r"^[A-Z]{3}$")

    location: TransactionLocation | None = None
    fraud_label: bool | None = None

    @field_validator("timestamp")
    @classmethod
    def require_timezone_aware_timestamp(
        cls,
        value: datetime,
    ) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("timestamp must be timezone-aware")

        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_transaction_destination(self) -> "NormalizedTransaction":
        if self.destination_account_id is None and self.merchant_id is None:
            raise ValueError(
                "A transaction must have either a destination account or a merchant"
            )

        return self


class TransactionResponse(BaseModel):
    """API response after accepting a transaction."""

    model_config = ConfigDict(extra="forbid")

    transaction_id: Identifier
    status: Literal["accepted", "duplicate"]
    message: str
