import sqlite3
import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "orchestrator.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_connection():
    """Returns a new SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Creates all tables if they don't already exist. Safe to call on every startup."""
    conn = get_connection()
    
    # Check if schema.sql exists
    if os.path.exists(SCHEMA_PATH):
        with open(SCHEMA_PATH, "r") as f:
            conn.executescript(f.read())
    else:
        # Create tables directly if schema.sql doesn't exist
        _create_tables(conn)
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")


def _create_tables(conn):
    """Create tables directly if schema.sql doesn't exist."""
    cursor = conn.cursor()
    
    # Create monitoring_logs table (existing)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitoring_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            cpu_usage REAL DEFAULT 0,
            memory_usage REAL DEFAULT 0,
            requests_per_sec REAL DEFAULT 0,
            response_time_ms REAL DEFAULT 0
        )
    ''')
    
    # Create decisions table (existing - enhanced)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            chosen_strategy TEXT NOT NULL,
            action TEXT NOT NULL,
            explanation TEXT,
            score_fixed_rule INTEGER DEFAULT 0,
            score_single_objective INTEGER DEFAULT 0,
            score_context_aware_mo INTEGER DEFAULT 0,
            cost_impact REAL DEFAULT 0,
            carbon_impact REAL DEFAULT 0,
            latency_impact REAL DEFAULT 0,
            action_type TEXT DEFAULT 'maintain',
            chosen_score INTEGER DEFAULT 0,
            weights_json TEXT,
            state_json TEXT,
            all_strategies_json TEXT
        )
    ''')
    
    # Create audit_trail table (existing - enhanced)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_trail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            time TEXT NOT NULL,
            date TEXT NOT NULL,
            action TEXT NOT NULL,
            action_type TEXT DEFAULT 'maintain',
            strategy TEXT NOT NULL,
            strategy_label TEXT DEFAULT 'Unknown Strategy',
            score INTEGER DEFAULT 0,
            explanation TEXT,
            cost_impact REAL DEFAULT 0,
            carbon_impact REAL DEFAULT 0,
            latency_impact REAL DEFAULT 0,
            cost_formatted TEXT,
            carbon_formatted TEXT,
            latency_formatted TEXT,
            weights_cost REAL DEFAULT 0.33,
            weights_carbon REAL DEFAULT 0.33,
            weights_latency REAL DEFAULT 0.34,
            state_json TEXT
        )
    ''')
    
    # Create experiment_results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS experiment_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scenario TEXT NOT NULL,
            strategy TEXT NOT NULL,
            cost_saved REAL DEFAULT 0,
            carbon_saved REAL DEFAULT 0,
            latency_penalty REAL DEFAULT 0,
            timestamp TEXT NOT NULL
        )
    ''')


# ============ EXISTING FUNCTIONS (KEEP AS IS) ============

def insert_monitoring_log(conn, entry: dict):
    conn.execute(
        "INSERT INTO monitoring_logs (timestamp, cpu_usage, memory_usage, requests_per_sec, response_time_ms) "
        "VALUES (?, ?, ?, ?, ?)",
        (entry["timestamp"], entry["cpu_usage"], entry.get("memory_usage"),
         entry.get("requests_per_sec", entry.get("requests_per_second", 0)), 
         entry.get("response_time_ms", entry.get("latency_ms", 0))),
    )
    conn.commit()


def get_recent_monitoring_logs(conn, limit=50):
    rows = conn.execute(
        "SELECT * FROM monitoring_logs ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(r) for r in reversed(rows)]


def insert_decision(conn, decision: dict):
    """Insert a decision into the database (enhanced version)."""
    scores = decision.get("scores", {})
    impact = decision.get("impact", {})
    weights = decision.get("weights", {})
    state = decision.get("state", {})
    all_strategies = decision.get("all_strategies", {})
    
    conn.execute(
        """INSERT INTO decisions
           (timestamp, chosen_strategy, action, action_type, explanation,
            score_fixed_rule, score_single_objective, score_context_aware_mo,
            chosen_score, cost_impact, carbon_impact, latency_impact,
            weights_json, state_json, all_strategies_json)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            decision.get("timestamp", datetime.now().isoformat()),
            decision.get("chosen_strategy", "context_aware_mo"),
            decision.get("action", ""),
            decision.get("action_type", "maintain"),
            decision.get("explanation", ""),
            scores.get("fixed_rule", 0),
            scores.get("single_objective", 0),
            scores.get("context_aware_mo", 0),
            decision.get("score", 0),
            impact.get("cost", 0),
            impact.get("carbon", 0),
            impact.get("latency", 0),
            json.dumps(weights),
            json.dumps(state),
            json.dumps(all_strategies)
        ),
    )
    conn.commit()


def insert_audit_entry(conn, entry: dict):
    """Insert an audit entry into the database (enhanced version)."""
    impact = entry.get("impact", {})
    impact_formatted = entry.get("impact_formatted", {})
    weights = entry.get("weights", {})
    state = entry.get("state", {})
    
    conn.execute(
        """INSERT INTO audit_trail 
           (timestamp, time, date, action, action_type, strategy, strategy_label,
            score, explanation,
            cost_impact, carbon_impact, latency_impact,
            cost_formatted, carbon_formatted, latency_formatted,
            weights_cost, weights_carbon, weights_latency,
            state_json)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            entry.get("timestamp", datetime.now().isoformat()),
            entry.get("time", datetime.now().strftime("%H:%M:%S")),
            entry.get("date", datetime.now().strftime("%Y-%m-%d")),
            entry.get("action", ""),
            entry.get("action_type", "maintain"),
            entry.get("strategy", "unknown"),
            entry.get("strategy_label", "Unknown Strategy"),
            entry.get("score", 0),
            entry.get("explanation", ""),
            impact.get("cost", 0),
            impact.get("carbon", 0),
            impact.get("latency", 0),
            impact_formatted.get("cost", ""),
            impact_formatted.get("carbon", ""),
            impact_formatted.get("latency", ""),
            weights.get("cost", 0.33),
            weights.get("carbon", 0.33),
            weights.get("latency", 0.34),
            json.dumps(state) if state else None
        ),
    )
    conn.commit()


def get_audit_history(conn, limit=25):
    """Get audit history (existing function - enhanced)."""
    rows = conn.execute(
        "SELECT * FROM audit_trail ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    
    entries = []
    for row in rows:
        entry = dict(row)
        # Reconstruct nested structures for frontend
        entry["impact"] = {
            "cost": entry.pop("cost_impact", 0),
            "carbon": entry.pop("carbon_impact", 0),
            "latency": entry.pop("latency_impact", 0)
        }
        entry["impact_formatted"] = {
            "cost": entry.pop("cost_formatted", ""),
            "carbon": entry.pop("carbon_formatted", ""),
            "latency": entry.pop("latency_formatted", "")
        }
        entry["weights"] = {
            "cost": entry.pop("weights_cost", 0.33),
            "carbon": entry.pop("weights_carbon", 0.33),
            "latency": entry.pop("weights_latency", 0.34)
        }
        
        # Parse state JSON if exists
        state_json = entry.pop("state_json", None)
        if state_json:
            entry["state"] = json.loads(state_json)
        else:
            entry["state"] = {}
        
        entries.append(entry)
    
    return entries


# ============ NEW FUNCTIONS FOR FRONTEND API ============

def get_audit_entries(
    limit: int = 50,
    offset: int = 0,
    strategy: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Dict[str, Any]]:
    """
    Get audit entries with pagination and filters.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT * FROM audit_trail 
            WHERE 1=1
        '''
        params = []
        
        if strategy:
            query += " AND strategy_label = ?"
            params.append(strategy)
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date.isoformat())
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date.isoformat())
        
        query += " ORDER BY id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        entries = []
        for row in rows:
            entry = dict(row)
            # Reconstruct nested structures
            entry["impact"] = {
                "cost": entry.pop("cost_impact", 0),
                "carbon": entry.pop("carbon_impact", 0),
                "latency": entry.pop("latency_impact", 0)
            }
            entry["impact_formatted"] = {
                "cost": entry.pop("cost_formatted", ""),
                "carbon": entry.pop("carbon_formatted", ""),
                "latency": entry.pop("latency_formatted", "")
            }
            entry["weights"] = {
                "cost": entry.pop("weights_cost", 0.33),
                "carbon": entry.pop("weights_carbon", 0.33),
                "latency": entry.pop("weights_latency", 0.34)
            }
            
            state_json = entry.pop("state_json", None)
            if state_json:
                entry["state"] = json.loads(state_json)
            else:
                entry["state"] = {}
            
            entries.append(entry)
        
        return entries
        
    except Exception as e:
        logger.error(f"Error getting audit entries: {e}")
        return []


def get_audit_stats() -> Dict[str, Any]:
    """
    Get audit statistics.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Total decisions
        cursor.execute("SELECT COUNT(*) as total FROM audit_trail")
        total = cursor.fetchone()["total"]
        
        # Cost saved (sum of negative cost impacts)
        cursor.execute("SELECT SUM(cost_impact) as cost_saved FROM audit_trail WHERE cost_impact < 0")
        cost_row = cursor.fetchone()
        cost_saved = abs(cost_row["cost_saved"]) if cost_row and cost_row["cost_saved"] else 0
        
        # Carbon saved (sum of negative carbon impacts)
        cursor.execute("SELECT SUM(carbon_impact) as carbon_saved FROM audit_trail WHERE carbon_impact < 0")
        carbon_row = cursor.fetchone()
        carbon_saved = abs(carbon_row["carbon_saved"]) if carbon_row and carbon_row["carbon_saved"] else 0
        
        # Average latency
        cursor.execute("SELECT AVG(latency_impact) as avg_latency FROM audit_trail")
        latency_row = cursor.fetchone()
        avg_latency = latency_row["avg_latency"] if latency_row and latency_row["avg_latency"] else 0
        
        # Strategies used
        cursor.execute("""
            SELECT strategy_label, COUNT(*) as count 
            FROM audit_trail 
            WHERE strategy_label IS NOT NULL
            GROUP BY strategy_label
        """)
        strategy_rows = cursor.fetchall()
        strategies_used = {row["strategy_label"]: row["count"] for row in strategy_rows}
        
        # Average score
        cursor.execute("SELECT AVG(score) as avg_score FROM audit_trail")
        score_row = cursor.fetchone()
        avg_score = score_row["avg_score"] if score_row and score_row["avg_score"] else 0
        
        conn.close()
        
        return {
            "total_decisions": total,
            "total_cost_saved": round(cost_saved, 2),
            "total_carbon_saved": round(carbon_saved, 2),
            "average_latency": round(avg_latency, 1),
            "strategies_used": strategies_used,
            "average_score": round(avg_score, 1)
        }
        
    except Exception as e:
        logger.error(f"Error getting audit stats: {e}")
        return {
            "total_decisions": 0,
            "total_cost_saved": 0,
            "total_carbon_saved": 0,
            "average_latency": 0,
            "strategies_used": {},
            "average_score": 0
        }


def clear_audit_table():
    """
    Clear all audit data (admin only).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM audit_trail")
        cursor.execute("DELETE FROM decisions")
        
        conn.commit()
        conn.close()
        
        logger.info("Audit data cleared")
        
    except Exception as e:
        logger.error(f"Error clearing audit data: {e}")
        raise


def get_monitoring_history(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Get monitoring history.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM monitoring_logs 
            ORDER BY id DESC LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
        
    except Exception as e:
        logger.error(f"Error getting monitoring history: {e}")
        return []


def get_audit_history_count() -> int:
    """
    Get total count of audit entries.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM audit_trail")
        total = cursor.fetchone()["total"]
        conn.close()
        return total
        
    except Exception as e:
        logger.error(f"Error getting audit count: {e}")
        return 0