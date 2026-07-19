CREATE TABLE IF NOT EXISTS monitoring_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    cpu_usage REAL,
    memory_usage REAL,
    requests_per_sec INTEGER,
    response_time_ms REAL
);

CREATE TABLE IF NOT EXISTS carbon_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    region TEXT,
    carbon_intensity REAL,
    unit TEXT
);

CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    chosen_strategy TEXT,
    action TEXT,
    explanation TEXT,
    score_fixed_rule REAL,
    score_single_objective REAL,
    score_context_aware_mo REAL,
    cost_impact REAL,
    carbon_impact REAL,
    latency_impact REAL,
    action_type TEXT DEFAULT 'maintain',
    chosen_score INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS audit_trail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    time TEXT NOT NULL,
    date TEXT,
    action TEXT,
    action_type TEXT DEFAULT 'maintain',
    strategy TEXT,
    strategy_label TEXT,
    score INTEGER DEFAULT 0,
    explanation TEXT,
    cost_impact REAL,
    carbon_impact REAL,
    latency_impact REAL,
    cost_formatted TEXT,
    carbon_formatted TEXT,
    latency_formatted TEXT,
    weights_cost REAL DEFAULT 0.33,
    weights_carbon REAL DEFAULT 0.33,
    weights_latency REAL DEFAULT 0.34,
    state_json TEXT
);