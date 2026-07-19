import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from state import app_state
from database.db_connection import init_db, get_connection, insert_monitoring_log
from agents.monitoring_agent import collect_live_metrics
from agents.prediction_agent import predict_traffic
from agents.decision_agent import make_decision
from agents.action_agent import simulate_action
from agents.audit_agent import record_decision
from utils.carbon_api_client import get_carbon_intensity

from api import monitoring_routes, carbon_routes, prediction_routes, decision_routes, audit_routes, experiments_routes

POLL_INTERVAL_SECONDS = 3
MAX_HISTORY = 60


async def agent_loop():
    """
    The continuous background pipeline: Monitoring -> Prediction -> Decision
    -> Action -> Audit, running forever regardless of whether the dashboard
    is even open. This is what makes the system "real-time" rather than
    request-triggered.
    """
    conn = get_connection()
    while True:
        try:
            monitoring = collect_live_metrics()
            app_state.monitoring_history.append(monitoring)
            app_state.monitoring_history = app_state.monitoring_history[-MAX_HISTORY:]
            app_state.latest_monitoring = monitoring
            insert_monitoring_log(conn, monitoring)

            carbon = get_carbon_intensity()
            app_state.latest_carbon = carbon

            prediction = predict_traffic(app_state.monitoring_history)
            app_state.latest_prediction = prediction

            decision = make_decision(monitoring, carbon, prediction)
            app_state.latest_decision = decision

            action_result = simulate_action(decision)
            record_decision(conn, decision, action_result)

        except Exception as e:
            # A single bad cycle should never crash the whole background loop
            print(f"[agent_loop] error: {e}")

        await asyncio.sleep(POLL_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = asyncio.create_task(agent_loop())
    yield
    task.cancel()


app = FastAPI(title="Cloud Orchestrator (FORESIGHT) API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(monitoring_routes.router, prefix="/api")
app.include_router(carbon_routes.router, prefix="/api")
app.include_router(prediction_routes.router, prefix="/api")
app.include_router(decision_routes.router, prefix="/api")
app.include_router(audit_routes.router, prefix="/api")
app.include_router(experiments_routes.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "FORESIGHT backend is running", "time": datetime.now().isoformat()}
