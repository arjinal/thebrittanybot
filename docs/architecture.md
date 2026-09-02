# Crypto bot architecture

The system is a modular monolith: one deployable application with hard module
boundaries. That keeps operation simple while preventing strategy, research,
and execution responsibilities from becoming entangled.

```mermaid
flowchart TB
    EXT[Free external crypto feeds] --> RAW[(Immutable raw events)]
    RH[Robinhood quotes, account, orders, and fills] --> RAW
    RH --> STATE[(Live transactional state)]
    RAW --> NORMAL[Normalization and data-quality checks]
    NORMAL --> HISTORY[(DuckDB and Parquet research history)]
    NORMAL --> HEALTH{Data-health gate}

    HISTORY --> TEST[Backtest and walk-forward evaluation]
    AI[GPT-assisted research, no broker credentials] --> CAND[Challengers]
    CAND --> TEST --> SHADOW[Shadow trading]
    SHADOW --> PROMOTE{Human promotion gate}
    PROMOTE --> CHAMP[Approved champion]

    HEALTH --> FEATURES[Live features]
    CHAMP --> STRATEGY[Champion strategy]
    FEATURES --> STRATEGY
    STRATEGY --> INTENT[Structured order intent]
    INTENT --> RISK{Deterministic risk gate}
    POLICY[Immutable risk policy] --> RISK
    STATE --> RISK
    RISK -->|Approved| EXEC[Single execution writer]
    EXEC --> API[Robinhood Crypto API]
    API --> RECON[Fill and balance reconciliation]
    RECON --> STATE
    RECON --> RAW

    INTENT --> AUDIT[(Append-only audit log)]
    RISK --> AUDIT
    RECON --> AUDIT
    KILL[Manual and automatic kill switch] --> RISK
```

## Module boundaries

- **Data:** adapters, normalized events, timestamp alignment, and health checks.
- **Strategy:** pure decision logic that returns an order intent.
- **Risk:** deterministic policy that returns an approval or rejection.
- **Execution:** the only module allowed to hold broker credentials or place an
  order.
- **Research:** backtests, challengers, evaluations, and promotion evidence.
- **Monitoring:** audit records, alerts, reconciliation, and kill-switch state.

## Initial data bottlenecks

- Robinhood execution prices can differ from external exchange prices.
- Free feeds have outages, rate limits, symbol differences, and uneven history.
- A candle does not reveal the exact spread or fill available at decision time.
- Backtests need point-in-time fees, latency, spread, and rejected-order models.
- Local collection must run long enough to build trustworthy execution-aware
  history.

The live loop must fail closed: stale, missing, or materially conflicting data
blocks new orders rather than asking the strategy to guess.
