# The Brittany Bot

An experimental, safety-first cryptocurrency trading system built around a
strict separation between research, risk control, and broker execution.

> [!WARNING]
> This repository does not currently place trades. It is an architecture
> scaffold, not financial advice or a promise of profitability.

## Design rules

- Strategy code produces structured order intents; it never talks to a broker.
- A deterministic risk gate approves or rejects every intent.
- Exactly one execution component is allowed to submit orders.
- GPT-assisted research can propose challengers but cannot change hard risk
  limits, promote itself, or access broker credentials.
- Raw market events and trading decisions are append-only and auditable.
- Live credentials, account state, logs, and market-data archives stay local.

See [the architecture](docs/architecture.md) for the system boundaries.

## Repository layout

```text
config/                 Safe configuration templates
docs/                   Architecture and operating documentation
src/thebrittanybot/     Python package
tests/                  Automated tests
data/                   Local market data (ignored)
logs/                   Local logs (ignored)
state/                  Local databases and runtime state (ignored)
```

## Local setup

Python 3.11 or newer is recommended.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m unittest discover -s tests
```

Copy the templates before adding local settings:

```powershell
Copy-Item .env.example .env
Copy-Item config\settings.example.toml config\settings.local.toml
```

Both destination files are ignored by Git. Trading remains disabled in the
example configuration.

## Planned build order

1. Data ingestion, normalization, and data-health checks
2. Replayable event storage and historical research dataset
3. Backtester with realistic fees, spread, slippage, and latency
4. Deterministic risk engine with property-based tests
5. Paper/shadow execution and reconciliation
6. Robinhood Crypto adapter with trading disabled by default
7. Small, manually approved live canary

## Security

Never commit API keys, private keys, `.env`, local configuration, account
exports, trading logs, or database files. If a secret is committed, assume it
is compromised and rotate it immediately; deleting it in a later commit is not
enough.
