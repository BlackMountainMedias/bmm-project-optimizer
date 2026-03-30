#!/usr/bin/env python3
"""Simulation engine for ICI construction project scenarios.

Generates realistic budget/actuals data with configurable failure modes,
runs early-detection analysis, and quantifies the dollar value of catching
problems early vs. discovering them late.

Output: CSV results + summary stats for pitch deck and sales materials.
"""
import csv
import json
import math
import os
import random
from dataclasses import dataclass, field, asdict
from typing import List, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".tmp", "simulations")

PHASES = ["Sitework", "Structural", "Mechanical", "Electrical", "Finishes"]

COST_CATEGORIES = ["Labor", "Materials", "Equipment", "Subcontractor"]

# Realistic line items per phase/category
LINE_ITEMS = {
    "Sitework": {
        "Labor": ["Excavation crew", "Grading crew", "Paving crew"],
        "Materials": ["Aggregate base", "Asphalt", "Concrete curbs"],
        "Equipment": ["Excavator rental", "Grader rental", "Compactor rental"],
        "Subcontractor": ["Surveying", "Environmental remediation"],
    },
    "Structural": {
        "Labor": ["Formwork crew", "Rebar crew", "Steel erection crew"],
        "Materials": ["Structural steel", "Rebar", "Concrete"],
        "Equipment": ["Crane rental", "Concrete pump rental"],
        "Subcontractor": ["Steel fabrication", "Concrete testing"],
    },
    "Mechanical": {
        "Labor": ["HVAC install crew", "Plumbing crew", "Fire protection crew"],
        "Materials": ["HVAC units", "Piping", "Fire suppression system"],
        "Equipment": ["Lifts and rigging", "Pipe threading machine"],
        "Subcontractor": ["Controls programming", "Insulation contractor"],
    },
    "Electrical": {
        "Labor": ["Electrical rough-in crew", "Panel install crew", "Low voltage crew"],
        "Materials": ["Wire and cable", "Panels and breakers", "Lighting fixtures"],
        "Equipment": ["Cable puller rental", "Lift rental"],
        "Subcontractor": ["Fire alarm contractor", "Generator install"],
    },
    "Finishes": {
        "Labor": ["Drywall crew", "Paint crew", "Flooring crew"],
        "Materials": ["Drywall and mud", "Paint and primer", "Flooring materials"],
        "Equipment": ["Scaffolding rental", "Floor prep equipment"],
        "Subcontractor": ["Tile contractor", "Millwork contractor"],
    },
}

# Failure mode definitions
FAILURE_MODES = [
    "on_track",
    "supplier_delay",
    "crew_inefficiency",
    "change_order_spiral",
    "material_price_spike",
    "scope_creep",
    "weather_delay",
    "rework",
]

# How each failure mode affects costs (multiplier ranges by category)
FAILURE_EFFECTS = {
    "on_track": {
        "Labor": (0.95, 1.03),
        "Materials": (0.97, 1.02),
        "Equipment": (0.98, 1.02),
        "Subcontractor": (0.97, 1.03),
    },
    "supplier_delay": {
        "Labor": (1.05, 1.25),      # idle crew waiting
        "Materials": (1.00, 1.08),   # materials themselves may not cost more
        "Equipment": (1.10, 1.30),   # extended rentals
        "Subcontractor": (1.00, 1.10),
    },
    "crew_inefficiency": {
        "Labor": (1.15, 1.40),       # primary impact
        "Materials": (1.02, 1.10),   # waste from rework
        "Equipment": (1.05, 1.15),   # longer on-site
        "Subcontractor": (0.98, 1.05),
    },
    "change_order_spiral": {
        "Labor": (1.10, 1.30),
        "Materials": (1.10, 1.35),
        "Equipment": (1.05, 1.15),
        "Subcontractor": (1.15, 1.45),  # subs hit hardest by scope changes
    },
    "material_price_spike": {
        "Labor": (0.98, 1.03),
        "Materials": (1.15, 1.45),   # primary impact
        "Equipment": (0.98, 1.02),
        "Subcontractor": (1.05, 1.15),
    },
    "scope_creep": {
        "Labor": (1.08, 1.25),
        "Materials": (1.10, 1.30),
        "Equipment": (1.05, 1.15),
        "Subcontractor": (1.10, 1.35),
    },
    "weather_delay": {
        "Labor": (1.08, 1.20),      # idle time + overtime to catch up
        "Materials": (1.00, 1.05),
        "Equipment": (1.10, 1.25),   # extended rentals
        "Subcontractor": (1.05, 1.15),
    },
    "rework": {
        "Labor": (1.20, 1.50),      # do it twice
        "Materials": (1.15, 1.40),   # wasted materials
        "Equipment": (1.05, 1.15),
        "Subcontractor": (1.10, 1.30),
    },
}

# Detection timing: how early (as % of project) the problem is caught
# Early = week 2-3 of a 20-week phase, Late = week 16-18
EARLY_DETECTION_SAVINGS = {
    "on_track": 0.0,
    "supplier_delay": 0.65,         # catch early, switch supplier, save 65% of overrun
    "crew_inefficiency": 0.55,      # retrain or swap crew, save 55%
    "change_order_spiral": 0.50,    # flag scope drift before it compounds
    "material_price_spike": 0.70,   # lock in price or find alternative early
    "scope_creep": 0.45,            # harder to reverse but early flag helps
    "weather_delay": 0.40,          # limited control but early schedule adjust helps
    "rework": 0.60,                 # catch quality issues before they propagate
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class LineItemResult:
    project_name: str
    project_value: float
    failure_mode: str
    phase: str
    cost_category: str
    line_item: str
    budgeted_amount: float
    actual_amount: float
    variance: float
    variance_pct: float
    rag_status: str


@dataclass
class ProjectResult:
    project_name: str
    project_value: float
    failure_mode: str
    total_budget: float
    total_actual: float
    total_variance: float
    variance_pct: float
    cost_without_detection: float
    cost_with_early_detection: float
    savings_from_early_detection: float
    savings_pct: float
    detection_week: int
    late_discovery_week: int
    line_items: List[LineItemResult] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------
def _budget_for_project(project_value: float) -> List[dict]:
    """Generate realistic budget line items for a given project value."""
    items = []
    # Distribute budget across phases (not evenly -- structural is biggest)
    phase_weights = {
        "Sitework": 0.10,
        "Structural": 0.35,
        "Mechanical": 0.22,
        "Electrical": 0.15,
        "Finishes": 0.18,
    }
    for phase, pw in phase_weights.items():
        phase_budget = project_value * pw
        # Distribute within phase across categories
        cat_weights = {"Labor": 0.40, "Materials": 0.30, "Equipment": 0.10, "Subcontractor": 0.20}
        for cat, cw in cat_weights.items():
            cat_budget = phase_budget * cw
            line_names = LINE_ITEMS[phase][cat]
            n = len(line_names)
            for i, name in enumerate(line_names):
                # Add some randomness to distribution
                share = (1.0 / n) * random.uniform(0.7, 1.3)
                amount = round(cat_budget * share, 2)
                items.append({
                    "phase": phase,
                    "cost_category": cat,
                    "line_item": name,
                    "budgeted_amount": amount,
                })
    return items


def simulate_project(
    project_name: str,
    project_value: float,
    failure_mode: str,
    affected_phases: List[str] = None,
    severity: float = 1.0,
) -> ProjectResult:
    """Simulate a single project with a given failure mode.

    Args:
        project_name: Display name for the project.
        project_value: Total contract value ($).
        failure_mode: One of FAILURE_MODES.
        affected_phases: Which phases are hit (default: random 1-3).
        severity: 0.5 = mild, 1.0 = typical, 1.5 = severe.
    """
    if failure_mode not in FAILURE_EFFECTS:
        raise ValueError(f"Unknown failure mode: {failure_mode}")

    budget_items = _budget_for_project(project_value)

    if affected_phases is None:
        n_affected = random.randint(1, 3)
        affected_phases = random.sample(PHASES, n_affected)

    effects = FAILURE_EFFECTS[failure_mode]
    line_results = []
    total_budget = 0.0
    total_actual = 0.0

    for item in budget_items:
        budgeted = item["budgeted_amount"]
        total_budget += budgeted

        phase = item["phase"]
        cat = item["cost_category"]

        if phase in affected_phases and failure_mode != "on_track":
            lo, hi = effects[cat]
            # Apply severity scaling
            multiplier = 1.0 + (random.uniform(lo, hi) - 1.0) * severity
        else:
            # Unaffected phase -- normal variance
            multiplier = random.uniform(0.96, 1.04)

        actual = round(budgeted * multiplier, 2)
        total_actual += actual

        variance = round(actual - budgeted, 2)
        variance_pct = round(variance / budgeted, 4) if budgeted > 0 else 0.0

        if variance_pct >= 0.10:
            rag = "red"
        elif variance_pct >= 0.05:
            rag = "yellow"
        else:
            rag = "green"

        lr = LineItemResult(
            project_name=project_name,
            project_value=project_value,
            failure_mode=failure_mode,
            phase=phase,
            cost_category=cat,
            line_item=item["line_item"],
            budgeted_amount=budgeted,
            actual_amount=actual,
            variance=variance,
            variance_pct=variance_pct,
            rag_status=rag,
        )
        line_results.append(lr)

    total_variance = round(total_actual - total_budget, 2)
    overall_pct = round(total_variance / total_budget, 4) if total_budget > 0 else 0.0

    # Calculate early detection value
    overrun = max(0, total_variance)
    savings_rate = EARLY_DETECTION_SAVINGS.get(failure_mode, 0.0)
    savings = round(overrun * savings_rate, 2)
    cost_with = round(total_actual - savings, 2)

    # Detection timing (in weeks, assuming 20-week project)
    project_weeks = max(12, int(project_value / 200000))  # rough heuristic
    detection_week = random.randint(2, max(3, project_weeks // 4))
    late_week = random.randint(int(project_weeks * 0.7), project_weeks)

    return ProjectResult(
        project_name=project_name,
        project_value=project_value,
        failure_mode=failure_mode,
        total_budget=round(total_budget, 2),
        total_actual=round(total_actual, 2),
        total_variance=total_variance,
        variance_pct=overall_pct,
        cost_without_detection=round(total_actual, 2),
        cost_with_early_detection=cost_with,
        savings_from_early_detection=savings,
        savings_pct=round(savings / total_budget, 4) if total_budget > 0 else 0.0,
        detection_week=detection_week,
        late_discovery_week=late_week,
        line_items=line_results,
    )


# ---------------------------------------------------------------------------
# Batch runner
# ---------------------------------------------------------------------------
# Realistic ICI project names
PROJECT_NAMES = [
    "Maple Ridge Office Tower", "Northgate Industrial Park",
    "City Centre Parking Structure", "Lakeview Medical Centre",
    "Harbour Point Condos", "Westfield Distribution Hub",
    "Provincial Courthouse Expansion", "Metro Transit Maintenance Facility",
    "Riverside Water Treatment Plant", "Kingsway Commercial Plaza",
    "Airport Cargo Terminal B", "University Science Building",
    "Downtown Hilton Renovation", "Regional Hospital Wing C",
    "Eastside Fire Station", "Heritage District Mixed-Use",
    "Tech Park Building 4", "Convention Centre Expansion",
    "Waterfront Promenade", "Industrial Waste Processing Facility",
    "Central Library Renovation", "Highway 7 Overpass",
    "Midtown Condo Tower A", "Southgate Retail Centre",
    "Greenfield Elementary School", "Power Substation Upgrade",
    "Port Authority Warehouse", "Federal Office Building Retrofit",
    "Luxury Resort Phase 2", "Municipal Aquatic Centre",
]


def run_batch(
    n_projects: int = 500,
    seed: int = 42,
) -> List[ProjectResult]:
    """Run a batch of simulated projects across various scenarios."""
    random.seed(seed)
    results = []

    # Project value distribution (realistic ICI spread)
    value_ranges = [
        (500_000, 2_000_000, 0.25),     # small projects
        (2_000_000, 8_000_000, 0.35),    # mid-size
        (8_000_000, 25_000_000, 0.25),   # large
        (25_000_000, 50_000_000, 0.15),  # mega
    ]

    # Failure mode distribution (realistic -- most projects have issues)
    mode_weights = [
        ("on_track", 0.15),
        ("supplier_delay", 0.15),
        ("crew_inefficiency", 0.15),
        ("change_order_spiral", 0.12),
        ("material_price_spike", 0.10),
        ("scope_creep", 0.12),
        ("weather_delay", 0.11),
        ("rework", 0.10),
    ]
    modes, weights = zip(*mode_weights)

    for i in range(n_projects):
        # Pick project value
        r = random.random()
        cumulative = 0.0
        project_value = 5_000_000  # fallback
        for lo, hi, w in value_ranges:
            cumulative += w
            if r <= cumulative:
                project_value = round(random.uniform(lo, hi), -3)  # round to nearest $1K
                break

        # Pick failure mode
        failure_mode = random.choices(modes, weights=weights, k=1)[0]

        # Pick severity (0.5 to 1.5, normally distributed around 1.0)
        severity = max(0.3, min(2.0, random.gauss(1.0, 0.3)))

        # Pick project name
        name_base = PROJECT_NAMES[i % len(PROJECT_NAMES)]
        suffix = f" (Sim {i + 1})" if i >= len(PROJECT_NAMES) else ""
        name = f"{name_base}{suffix}"

        result = simulate_project(
            project_name=name,
            project_value=project_value,
            failure_mode=failure_mode,
            severity=severity,
        )
        results.append(result)

    return results


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------
def write_results(results: List[ProjectResult]):
    """Write simulation results to CSV and JSON summary."""
    os.makedirs(OUT_DIR, exist_ok=True)

    # 1. Project-level summary CSV
    summary_path = os.path.join(OUT_DIR, "project_summary.csv")
    fields = [
        "project_name", "project_value", "failure_mode",
        "total_budget", "total_actual", "total_variance", "variance_pct",
        "cost_without_detection", "cost_with_early_detection",
        "savings_from_early_detection", "savings_pct",
        "detection_week", "late_discovery_week",
    ]
    with open(summary_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in results:
            row = {k: getattr(r, k) for k in fields}
            w.writerow(row)

    # 2. Line-item detail CSV (for feeding into the dashboard)
    detail_path = os.path.join(OUT_DIR, "line_item_detail.csv")
    detail_fields = [
        "project_name", "project_value", "failure_mode",
        "phase", "cost_category", "line_item",
        "budgeted_amount", "actual_amount", "variance", "variance_pct", "rag_status",
    ]
    with open(detail_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=detail_fields)
        w.writeheader()
        for r in results:
            for lr in r.line_items:
                w.writerow(asdict(lr))

    # 3. Aggregate stats JSON
    stats = compute_stats(results)
    stats_path = os.path.join(OUT_DIR, "simulation_stats.json")
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)

    # 4. Budget/Actuals CSVs compatible with dashboard
    budget_path = os.path.join(OUT_DIR, "sim_budget.csv")
    actuals_path = os.path.join(OUT_DIR, "sim_actuals.csv")

    with open(budget_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["project_name", "phase", "cost_category", "line_item", "budgeted_amount"])
        w.writeheader()
        for r in results:
            for lr in r.line_items:
                w.writerow({
                    "project_name": lr.project_name,
                    "phase": lr.phase,
                    "cost_category": lr.cost_category,
                    "line_item": lr.line_item,
                    "budgeted_amount": lr.budgeted_amount,
                })

    with open(actuals_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["project_name", "phase", "cost_category", "line_item", "actual_amount"])
        w.writeheader()
        for r in results:
            for lr in r.line_items:
                w.writerow({
                    "project_name": lr.project_name,
                    "phase": lr.phase,
                    "cost_category": lr.cost_category,
                    "line_item": lr.line_item,
                    "actual_amount": lr.actual_amount,
                })

    print(f"Project summary:  {summary_path}")
    print(f"Line item detail: {detail_path}")
    print(f"Dashboard budget: {budget_path}")
    print(f"Dashboard actuals: {actuals_path}")
    print(f"Stats:            {stats_path}")

    return stats


def compute_stats(results: List[ProjectResult]) -> dict:
    """Compute aggregate statistics across all simulations."""
    n = len(results)
    if n == 0:
        return {}

    total_budget = sum(r.total_budget for r in results)
    total_actual = sum(r.total_actual for r in results)
    total_overrun = sum(max(0, r.total_variance) for r in results)
    total_savings = sum(r.savings_from_early_detection for r in results)

    # Projects with overruns
    overrun_projects = [r for r in results if r.total_variance > 0]
    on_track = [r for r in results if r.failure_mode == "on_track"]

    # By failure mode
    by_mode = {}
    for mode in FAILURE_MODES:
        mode_results = [r for r in results if r.failure_mode == mode]
        if not mode_results:
            continue
        mode_overrun = sum(max(0, r.total_variance) for r in mode_results)
        mode_savings = sum(r.savings_from_early_detection for r in mode_results)
        avg_variance = sum(r.variance_pct for r in mode_results) / len(mode_results)
        by_mode[mode] = {
            "count": len(mode_results),
            "avg_variance_pct": round(avg_variance * 100, 1),
            "total_overrun": round(mode_overrun, 2),
            "total_savings_with_detection": round(mode_savings, 2),
            "avg_savings_per_project": round(mode_savings / len(mode_results), 2),
        }

    # By project size
    size_buckets = [
        ("Under $2,000,000", 0, 2_000_000),
        ("$2,000,000 - $8,000,000", 2_000_000, 8_000_000),
        ("$8,000,000 - $25,000,000", 8_000_000, 25_000_000),
        ("Over $25,000,000", 25_000_000, float("inf")),
    ]
    by_size = {}
    for label, lo, hi in size_buckets:
        bucket = [r for r in results if lo <= r.project_value < hi]
        if not bucket:
            continue
        bucket_savings = sum(r.savings_from_early_detection for r in bucket)
        bucket_overrun = sum(max(0, r.total_variance) for r in bucket)
        by_size[label] = {
            "count": len(bucket),
            "total_overrun": round(bucket_overrun, 2),
            "total_savings": round(bucket_savings, 2),
            "avg_savings_per_project": round(bucket_savings / len(bucket), 2),
        }

    # Top 10 worst projects
    worst = sorted(results, key=lambda r: r.total_variance, reverse=True)[:10]
    top_10_worst = [{
        "project_name": r.project_name,
        "project_value": r.project_value,
        "failure_mode": r.failure_mode,
        "overrun": round(r.total_variance, 2),
        "overrun_pct": round(r.variance_pct * 100, 1),
        "savings_if_caught_early": round(r.savings_from_early_detection, 2),
    } for r in worst]

    return {
        "simulation_count": n,
        "total_portfolio_budget": round(total_budget, 2),
        "total_portfolio_actual": round(total_actual, 2),
        "total_overrun": round(total_overrun, 2),
        "total_savings_with_early_detection": round(total_savings, 2),
        "avg_savings_per_project": round(total_savings / n, 2),
        "projects_with_overruns": len(overrun_projects),
        "projects_on_track": len(on_track),
        "pct_projects_over_budget": round(len(overrun_projects) / n * 100, 1),
        "avg_overrun_pct": round(
            sum(r.variance_pct for r in overrun_projects) / len(overrun_projects) * 100, 1
        ) if overrun_projects else 0,
        "by_failure_mode": by_mode,
        "by_project_size": by_size,
        "top_10_worst_projects": top_10_worst,
    }


def print_summary(stats: dict):
    """Print a human-readable summary to stdout."""
    print("\n" + "=" * 65)
    print("  SIMULATION RESULTS")
    print("=" * 65)
    print(f"  Projects simulated:        {stats['simulation_count']}")
    print(f"  Total portfolio budget:    ${stats['total_portfolio_budget']:,.0f}")
    print(f"  Total portfolio actual:    ${stats['total_portfolio_actual']:,.0f}")
    print(f"  Total overrun:             ${stats['total_overrun']:,.0f}")
    print(f"  Projects over budget:      {stats['projects_with_overruns']} ({stats['pct_projects_over_budget']}%)")
    print(f"  Avg overrun (over-budget): {stats['avg_overrun_pct']}%")
    print()
    print(f"  EARLY DETECTION VALUE")
    print(f"  Total savings possible:    ${stats['total_savings_with_early_detection']:,.0f}")
    print(f"  Avg savings per project:   ${stats['avg_savings_per_project']:,.0f}")
    print()

    print("  BY FAILURE MODE:")
    for mode, data in stats["by_failure_mode"].items():
        print(f"    {mode:25s}  {data['count']:3d} projects  "
              f"avg {data['avg_variance_pct']:+.1f}%  "
              f"savings ${data['avg_savings_per_project']:,.0f}/project")

    print()
    print("  BY PROJECT SIZE:")
    for size, data in stats["by_project_size"].items():
        print(f"    {size:30s}  {data['count']:3d} projects  "
              f"avg savings ${data['avg_savings_per_project']:,.0f}/project")

    print()
    print("  TOP 5 WORST PROJECTS:")
    for p in stats["top_10_worst_projects"][:5]:
        print(f"    {p['project_name']:40s}  "
              f"${p['project_value']:>12,.0f} value  "
              f"{p['overrun_pct']:+.1f}%  "
              f"${p['overrun']:>10,.0f} overrun  "
              f"${p['savings_if_caught_early']:>10,.0f} saveable")

    print("=" * 65)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Running 500 project simulations...")
    results = run_batch(n_projects=500, seed=42)
    stats = write_results(results)
    print_summary(stats)


if __name__ == "__main__":
    main()
