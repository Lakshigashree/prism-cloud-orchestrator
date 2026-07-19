# Cloud Orchestrator (FORESIGHT) — Backend

FastAPI backend implementing the 5-agent pipeline: Monitoring → Prediction →
Decision → Action → Audit.

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then edit .env with your real carbon API key
uvicorn main:app --reload --port 8000
```

Visit `http://127.0.0.1:8000/docs` for interactive API docs.

The frontend (Vite) proxies `/api/*` straight to this server — no CORS
setup needed if you're running both locally with the default ports.

## What's running

The moment the server starts, a background loop (`agent_loop` in `main.py`)
begins running every 3 seconds, forever — independent of whether the
dashboard is even open:

1. **Monitoring Agent** collects live metrics (from a real deployed app's
   `/metrics` endpoint if `MONITORED_APP_URL` is set in `.env`, otherwise
   from the built-in traffic simulator)
2. **Prediction Agent** forecasts the next 30 minutes using ARIMA
3. **Decision Agent** runs all 3 strategies (fixed-rule, single-objective,
   context-aware multi-objective) and picks the winner
4. **Action Agent** simulates the outcome (no real infrastructure touched)
5. **Audit Agent** logs everything to SQLite

## Using a real deployed app instead of the simulator

Add a `/metrics` endpoint to whatever app you deploy, using `psutil`:

```python
import psutil
from fastapi import FastAPI
app = FastAPI()

@app.get("/metrics")
def get_metrics():
    return {
        "cpu_usage": psutil.cpu_percent(interval=0.5),
        "memory_usage": psutil.virtual_memory().percent,
        "requests_per_sec": 0,       # increment this yourself via middleware
        "response_time_ms": 0,
    }
```

Then set `MONITORED_APP_URL=http://your-app-url/metrics` in `.env`.
Nothing else in the pipeline needs to change — real data will start
flowing automatically.

## Running the experiments (for your paper's Results section)

```bash
python experiments/run_experiments.py
```

This runs all 3 decision strategies against 3 traffic scenarios (Normal
Day, Traffic Spike, Low-Traffic Night) and writes
`experiments/results/latest_results.json`, which `/api/experiments/results`
serves directly to the frontend's Results page.

## API endpoints

| Route | Description |
|---|---|
| `GET /api/monitoring/live` | Latest monitoring reading |
| `GET /api/carbon` | Latest grid carbon intensity |
| `GET /api/prediction` | Traffic forecast, next 30 min |
| `GET /api/decision` | Current decision + comparison scores |
| `GET /api/audit/history` | Recent decision log |
| `GET /api/experiments/results` | Strategy comparison results |

## Folder structure

```
backend/
├── main.py                   # FastAPI app + background agent loop
├── state.py                  # shared in-memory state between loop and API routes
├── agents/                   # the 5 agents
│   └── decision_strategies/  # the 3 decision strategies being compared
├── api/                      # route handlers, one file per endpoint group
├── database/                 # SQLite schema + connection helpers
├── utils/                    # carbon API client
└── experiments/              # scenario definitions + the experiment runner
```
