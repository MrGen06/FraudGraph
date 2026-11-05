import pytest
from pydantic import ValidationError

from app.schemas.transactions import NormalizedTransaction


def valid_transaction() -> dict:
    return {
        "transaction_id": "TX001",
        "timestamp": "2026-10-24T10:00:00Z",
        "source_account_id": "A1",
        "destination_account_id": "A2",
        "user_id": "U1",
        "card_id": "C1",
        "device_id": "D1",
        "ip_id": "IP1",
        "merchant_id": "M1",
        "amount": 2500.0,
        "currency": "INR",
        "location": {
            "country": "IN",
            "region": "HR",
        },
        "fraud_label": None,
    }


def test_valid_transaction_is_accepted() -> None:
    transaction = NormalizedTransaction(**valid_transaction())

    assert transaction.transaction_id == "TX001"
    assert transaction.amount == 2500.0
    assert transaction.currency == "INR"
    assert transaction.timestamp.tzinfo is not None


def test_timestamp_is_normalized_to_utc() -> None:
    transaction = NormalizedTransaction(**valid_transaction())

    utc_offset = transaction.timestamp.utcoffset()
    assert utc_offset is not None
    assert utc_offset.total_seconds() == 0


def test_card_purchase_without_destination_is_accepted() -> None:
    data = valid_transaction()
    data["destination_account_id"] = None

    transaction = NormalizedTransaction(**data)

    assert transaction.destination_account_id is None
    assert transaction.merchant_id == "M1"


def test_naive_timestamp_is_rejected() -> None:
    data = valid_transaction()
    data["timestamp"] = "2026-10-24T10:00:00"

    with pytest.raises(ValidationError):
        NormalizedTransaction(**data)


@pytest.mark.parametrize("amount", [0, -100])
def test_invalid_amount_is_rejected(amount: float) -> None:
    data = valid_transaction()
    data["amount"] = amount

    with pytest.raises(ValidationError):
        NormalizedTransaction(**data)


def test_missing_destination_and_merchant_are_rejected() -> None:
    data = valid_transaction()
    data["destination_account_id"] = None
    data["merchant_id"] = None

    with pytest.raises(ValidationError):
        NormalizedTransaction(**data)


@pytest.mark.parametrize("currency", ["inr", "IN", "123", "USDD"])
def test_invalid_currency_is_rejected(currency: str) -> None:
    data = valid_transaction()
    data["currency"] = currency

    with pytest.raises(ValidationError):
        NormalizedTransaction(**data)


def test_unknown_field_is_rejected() -> None:
    data = valid_transaction()
    data["unexpected_field"] = "invalid"

    with pytest.raises(ValidationError):
        NormalizedTransaction(**data)


def test_country_code_is_normalized() -> None:
    data = valid_transaction()
    data["location"]["country"] = "in"

    transaction = NormalizedTransaction(**data)

    assert transaction.location is not None
    assert transaction.location.country == "IN"
