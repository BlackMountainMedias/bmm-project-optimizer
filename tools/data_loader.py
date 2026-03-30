"""CSV loading, validation, sample data generation for BMM Project Optimizer."""
import os
import pandas as pd
import numpy as np

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_data")

BUDGET_COLS = ["project_name", "phase", "cost_category", "line_item", "budgeted_amount"]
ACTUALS_COLS = ["project_name", "phase", "cost_category", "line_item", "actual_amount"]
CO_COLS = ["project_name", "co_number", "description", "cost_impact"]
SCHEDULE_COLS = ["project_name", "task_name", "planned_start", "planned_end"]
TIMECARD_COLS = ["project_name", "worker_name", "date", "hours"]
MATERIAL_COLS = ["project_name", "material", "quantity", "unit_cost"]


def load_csv(uploaded_file, required_cols):
    """Parse an uploaded CSV and validate columns. Returns (df, errors)."""
    errors = []
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        return None, [f"Could not read CSV: {e}"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        errors.append(f"Missing columns: {', '.join(missing)}")
        return None, errors
    # Coerce amount columns to numeric
    for col in df.columns:
        if "amount" in col:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            bad = df[col].isna().sum()
            if bad:
                errors.append(f"{bad} non-numeric values in '{col}' (set to 0)")
                df[col] = df[col].fillna(0)
    return df, errors


def load_sample_data():
    """Load the demo CSVs shipped with the app. Returns dict of all available data."""
    budget = pd.read_csv(os.path.join(SAMPLE_DIR, "demo_budget.csv"))
    actuals = pd.read_csv(os.path.join(SAMPLE_DIR, "demo_actuals.csv"))

    result = {"budget": budget, "actuals": actuals}

    co_path = os.path.join(SAMPLE_DIR, "demo_change_orders.csv")
    if os.path.exists(co_path):
        result["change_orders"] = pd.read_csv(co_path)

    sched_path = os.path.join(SAMPLE_DIR, "demo_schedule.csv")
    if os.path.exists(sched_path):
        result["schedule"] = pd.read_csv(sched_path)

    tc_path = os.path.join(SAMPLE_DIR, "demo_timecards.csv")
    if os.path.exists(tc_path):
        result["timecards"] = pd.read_csv(tc_path)

    mat_path = os.path.join(SAMPLE_DIR, "demo_materials.csv")
    if os.path.exists(mat_path):
        result["materials"] = pd.read_csv(mat_path)

    return result


def merge_budget_actuals(budget_df, actuals_df, change_orders_df=None):
    """Left join budget to actuals on composite key, compute variance.

    If change_orders_df is provided, stash approved CO totals per project
    for use in portfolio_summary — CO adjustment is applied at the project
    level, not per line item, to avoid double-counting.
    """
    key = ["project_name", "phase", "cost_category", "line_item"]
    merged = budget_df.merge(actuals_df, on=key, how="left")
    merged["actual_amount"] = merged["actual_amount"].fillna(0)
    merged["variance"] = merged["actual_amount"] - merged["budgeted_amount"]
    merged["variance_pct"] = merged["variance"] / merged["budgeted_amount"]

    # Stash CO project-level totals as metadata (not per-row)
    merged.attrs["co_by_project"] = {}
    if change_orders_df is not None and not change_orders_df.empty:
        co = change_orders_df.copy()
        co["cost_impact"] = pd.to_numeric(co["cost_impact"], errors="coerce").fillna(0)

        if "status" in co.columns:
            approved = co[co["status"].str.lower().str.strip() == "approved"]
        else:
            approved = co

        if not approved.empty:
            co_totals = approved.groupby("project_name")["cost_impact"].sum().to_dict()
            merged.attrs["co_by_project"] = co_totals

    return merged


def parse_schedule(schedule_df):
    """Parse schedule data — convert date columns, compute slippage metrics."""
    df = schedule_df.copy()
    date_cols = ["planned_start", "planned_end", "actual_start", "actual_end"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    if "pct_complete" in df.columns:
        df["pct_complete"] = pd.to_numeric(df["pct_complete"], errors="coerce").fillna(0)

    # Planned duration in days
    if "planned_start" in df.columns and "planned_end" in df.columns:
        df["planned_duration"] = (df["planned_end"] - df["planned_start"]).dt.days

    # Start slippage
    if "actual_start" in df.columns and "planned_start" in df.columns:
        df["start_slip_days"] = (df["actual_start"] - df["planned_start"]).dt.days

    # End slippage (only for completed tasks)
    if "actual_end" in df.columns and "planned_end" in df.columns:
        df["end_slip_days"] = (df["actual_end"] - df["planned_end"]).dt.days

    # For in-progress tasks: projected end based on % complete and elapsed time
    today = pd.Timestamp.now().normalize()
    if "actual_start" in df.columns and "pct_complete" in df.columns:
        in_progress = df["actual_start"].notna() & df["pct_complete"].between(1, 99)
        elapsed = (today - df["actual_start"]).dt.days
        # Projected total duration = elapsed / (pct_complete / 100)
        projected_total = np.where(
            in_progress & (df["pct_complete"] > 0),
            elapsed / (df["pct_complete"] / 100),
            np.nan,
        )
        df["projected_end"] = df["actual_start"] + pd.to_timedelta(projected_total, unit="D")
        df["projected_slip_days"] = np.where(
            in_progress,
            (df["projected_end"] - df["planned_end"]).dt.days,
            np.nan,
        )

    return df


def parse_timecards(timecards_df):
    """Parse timecard data — convert types, compute labor cost."""
    df = timecards_df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["hours"] = pd.to_numeric(df["hours"], errors="coerce").fillna(0)

    if "hourly_rate" in df.columns:
        df["hourly_rate"] = pd.to_numeric(df["hourly_rate"], errors="coerce").fillna(0)
        df["labor_cost"] = df["hours"] * df["hourly_rate"]
    if "overtime_hours" in df.columns:
        df["overtime_hours"] = pd.to_numeric(df["overtime_hours"], errors="coerce").fillna(0)
        if "hourly_rate" in df.columns:
            df["overtime_cost"] = df["overtime_hours"] * df["hourly_rate"] * 1.5

    return df


def parse_materials(materials_df):
    """Parse materials data — convert types, compute totals, flag delivery risk."""
    df = materials_df.copy()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce").fillna(0)

    if "total_cost" not in df.columns or df["total_cost"].isna().all():
        df["total_cost"] = df["quantity"] * df["unit_cost"]
    else:
        df["total_cost"] = pd.to_numeric(df["total_cost"], errors="coerce").fillna(
            df["quantity"] * df["unit_cost"]
        )

    date_cols = ["order_date", "delivery_date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Delivery lead time
    if "order_date" in df.columns and "delivery_date" in df.columns:
        df["lead_time_days"] = (df["delivery_date"] - df["order_date"]).dt.days

    # Flag late or at-risk deliveries
    today = pd.Timestamp.now().normalize()
    if "delivery_date" in df.columns and "status" in df.columns:
        status_lower = df["status"].str.lower().str.strip()
        df["delivery_risk"] = "On Track"
        # Backordered = high risk
        df.loc[status_lower == "backordered", "delivery_risk"] = "High Risk"
        # Past due and not delivered
        df.loc[
            (df["delivery_date"] < today) & (~status_lower.isin(["delivered"])),
            "delivery_risk",
        ] = "Overdue"
        # Delivering within 7 days and not yet delivered
        df.loc[
            (df["delivery_date"] <= today + pd.Timedelta(days=7))
            & (df["delivery_date"] >= today)
            & (~status_lower.isin(["delivered"])),
            "delivery_risk",
        ] = "Watch"

    return df
