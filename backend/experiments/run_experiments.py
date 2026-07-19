import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.decision_strategies import fixed_rule, single_objective, multi_objective
from experiments.scenarios.normal_day import normal_day
from experiments.scenarios.traffic_spike import traffic_spike
from experiments.scenarios.low_traffic_night import low_traffic_night

SCENARIOS = {
    "Normal Day": normal_day,
    "Traffic Spike": traffic_spike,
    "Low-Traffic Night": low_traffic_night,
}

STRATEGIES = {
    "Fixed-Rule": fixed_rule.decide,
    "Single-Objective": single_objective.decide,
    "Context-Aware MO": multi_objective.decide,
}


def run_strategy_on_scenario(decide_fn, states):
    total_cost, total_carbon, total_latency = 0.0, 0.0, 0.0
    for state in states:
        result = decide_fn(state)
        total_cost += result["cost_impact"]
        total_carbon += result["carbon_impact"]
        total_latency += result["latency_impact"]

    n = len(states)
    # Convert running totals into "% saved" (negative delta = savings) and
    # an average latency penalty in ms, matching the frontend's expected shape.
    cost_saved_pct = round(max(0, -total_cost) / n * 100, 1)
    carbon_saved_pct = round(max(0, -total_carbon) / n * 100, 1)
    latency_penalty_ms = round(max(0, total_latency) / n, 1)
    return cost_saved_pct, carbon_saved_pct, latency_penalty_ms


def main():
    scenario_names = list(SCENARIOS.keys())
    results = {"scenarios": scenario_names, "strategies": []}

    for strat_name, decide_fn in STRATEGIES.items():
        cost_list, carbon_list, latency_list = [], [], []
        for scenario_name, scenario_fn in SCENARIOS.items():
            states = scenario_fn()
            c, k, l = run_strategy_on_scenario(decide_fn, states)
            cost_list.append(c)
            carbon_list.append(k)
            latency_list.append(l)

        results["strategies"].append({
            "name": strat_name,
            "costSaved": cost_list,
            "carbonSaved": carbon_list,
            "latencyPenalty": latency_list,
        })

    out_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "latest_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Results written to {out_path}")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
