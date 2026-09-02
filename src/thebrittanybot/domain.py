"""Broker-independent domain messages shared across module boundaries."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum


class OrderSide(StrEnum):
    """The direction of a requested spot order."""

    BUY = "buy"
    SELL = "sell"


@dataclass(frozen=True, slots=True)
class OrderIntent:
    """A strategy proposal; it is not authorization to place an order."""

    intent_id: str
    strategy_version: str
    created_at: datetime
    symbol: str
    side: OrderSide
    notional_usd: Decimal
    reason_code: str

    def __post_init__(self) -> None:
        if self.notional_usd <= 0:
            raise ValueError("notional_usd must be positive")
        if self.created_at.tzinfo is None:
            raise ValueError("created_at must include a timezone")


@dataclass(frozen=True, slots=True)
class RiskDecision:
    """The deterministic risk gate's decision for one intent."""

    intent_id: str
    approved: bool
    reason_code: str
    policy_version: str
