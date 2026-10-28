# Trading Agent

A staged project to explore an AI-assisted Forex trading agent. Development starts with a local, non-executing application and automated tests.

## Current milestone: first working foundation

This repository currently provides:
- A small Python dashboard served locally.
- Clearly labelled fictional market values for UI and endpoint testing.
- JSON endpoints for health, application status and sample market data.
- Automated tests using Python's standard library.
- An explicit demo-only status: no broker connection and no order execution.

**Important:** sample prices are fictional, not current market quotes. This is not a trading system and does not provide trading signals or financial advice.

## Requirements

- Python 3.10 or newer
- No third-party Python packages required

## Run locally

From the repository root:

```bash
python app.py
```

Open http://127.0.0.1:8000 in your browser. Stop the server with Ctrl+C.

Optional environment variables:

- `TRADING_AGENT_HOST`: bind address (defaults to `127.0.0.1`, local machine only)
- `TRADING_AGENT_PORT`: port (defaults to `8000`)

Keep the default local bind address during development. Do not expose the development server directly to the public internet.

## API endpoints

| Path | Purpose |
| --- | --- |
| `/health` | Basic health response for local and future hosting checks |
| `/api/status` | Application mode and safety status |
| `/api/market-data` | Fictional, explicitly labelled sample values |

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Safety boundaries

- Demo mode only.
- No live market-data provider.
- No broker credentials or broker connection.
- No strategy, signal generation, order routing, or order execution.
- No live trading permission is implied by any future development milestone.

Any future market-data integration, strategy, simulation, broker integration or deployment should be introduced separately, tested, and documented. Broker connectivity and live orders require explicit owner approval and appropriate safety review.
