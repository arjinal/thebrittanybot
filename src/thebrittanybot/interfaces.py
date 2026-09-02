"""Contracts that keep strategy, risk, and execution independent."""

from typing import Protocol

from .domain import OrderIntent, RiskDecision


class Strategy(Protocol):
    """Creates proposals without broker or credential access."""

    def evaluate(self) -> OrderIntent | None: ...


class RiskGate(Protocol):
    """Applies non-learnable policy to a proposed order."""

    def evaluate(self, intent: OrderIntent) -> RiskDecision: ...


class BrokerExecutor(Protocol):
    """Single-writer boundary for broker interaction."""

    def submit(self, intent: OrderIntent, decision: RiskDecision) -> str: ...
