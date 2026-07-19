import sqlite3

conn = sqlite3.connect("data/orchestrator.db")
cursor = conn.cursor()

# Add columns to decisions
try:
    cursor.execute("ALTER TABLE decisions ADD COLUMN action_type TEXT DEFAULT 'maintain'")
    print("✅ Added action_type to decisions")
except:
    print("⚠️ action_type already exists")

try:
    cursor.execute("ALTER TABLE decisions ADD COLUMN chosen_score INTEGER DEFAULT 0")
    print("✅ Added chosen_score to decisions")
except:
    print("⚠️ chosen_score already exists")

# Add columns to audit_trail
try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN timestamp TEXT")
    print("✅ Added timestamp to audit_trail")
except:
    print("⚠️ timestamp already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN date TEXT")
    print("✅ Added date to audit_trail")
except:
    print("⚠️ date already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN action_type TEXT DEFAULT 'maintain'")
    print("✅ Added action_type to audit_trail")
except:
    print("⚠️ action_type already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN strategy_label TEXT")
    print("✅ Added strategy_label to audit_trail")
except:
    print("⚠️ strategy_label already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN score INTEGER DEFAULT 0")
    print("✅ Added score to audit_trail")
except:
    print("⚠️ score already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN explanation TEXT")
    print("✅ Added explanation to audit_trail")
except:
    print("⚠️ explanation already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN cost_impact REAL")
    print("✅ Added cost_impact to audit_trail")
except:
    print("⚠️ cost_impact already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN carbon_impact REAL")
    print("✅ Added carbon_impact to audit_trail")
except:
    print("⚠️ carbon_impact already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN latency_impact REAL")
    print("✅ Added latency_impact to audit_trail")
except:
    print("⚠️ latency_impact already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN cost_formatted TEXT")
    print("✅ Added cost_formatted to audit_trail")
except:
    print("⚠️ cost_formatted already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN carbon_formatted TEXT")
    print("✅ Added carbon_formatted to audit_trail")
except:
    print("⚠️ carbon_formatted already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN latency_formatted TEXT")
    print("✅ Added latency_formatted to audit_trail")
except:
    print("⚠️ latency_formatted already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN weights_cost REAL DEFAULT 0.33")
    print("✅ Added weights_cost to audit_trail")
except:
    print("⚠️ weights_cost already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN weights_carbon REAL DEFAULT 0.33")
    print("✅ Added weights_carbon to audit_trail")
except:
    print("⚠️ weights_carbon already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN weights_latency REAL DEFAULT 0.34")
    print("✅ Added weights_latency to audit_trail")
except:
    print("⚠️ weights_latency already exists")

try:
    cursor.execute("ALTER TABLE audit_trail ADD COLUMN state_json TEXT")
    print("✅ Added state_json to audit_trail")
except:
    print("⚠️ state_json already exists")

conn.commit()
conn.close()
print("\n✅ Database updated successfully!")