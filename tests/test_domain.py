from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thebrittanybot.domain import OrderIntent, OrderSide


class OrderIntentTests(unittest.TestCase):
    def test_accepts_positive_notional(self) -> None:
        intent = OrderIntent(
            intent_id="intent-1",
            strategy_version="test-v1",
            created_at=datetime.now(UTC),
            symbol="BTC-USD",
            side=OrderSide.BUY,
            notional_usd=Decimal("5.00"),
            reason_code="test",
        )

        self.assertEqual(intent.notional_usd, Decimal("5.00"))

    def test_rejects_nonpositive_notional(self) -> None:
        with self.assertRaisesRegex(ValueError, "must be positive"):
            OrderIntent(
                intent_id="intent-2",
                strategy_version="test-v1",
                created_at=datetime.now(UTC),
                symbol="BTC-USD",
                side=OrderSide.BUY,
                notional_usd=Decimal("0"),
                reason_code="test",
            )

    def test_rejects_naive_timestamp(self) -> None:
        with self.assertRaisesRegex(ValueError, "must include a timezone"):
            OrderIntent(
                intent_id="intent-2",
                strategy_version="test-v1",
                created_at=datetime.now(),
                symbol="BTC-USD",
                side=OrderSide.BUY,
                notional_usd=Decimal("5.00"),
                reason_code="test",
            )


if __name__ == "__main__":
    unittest.main()
