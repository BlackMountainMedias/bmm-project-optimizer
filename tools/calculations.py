"""Variance math, RAG status, summary rollups, outlier detection,
scoring, and analysis for change orders, schedule, labor, and materials."""
import pandas as pd
import numpy as np
from outlier_detection import detect_outliers, outlier_summary, outlier_by_project, outlier_by_category


def assign_rag(variance_pct, yellow=0.05, red=0.10):
    """Return 'green', 'yellow', or 'red' based on % over budget."""
    if variance_pct >= red:
        return "red"
    elif variance_pct >= yellow:
        return "yellow"
    return "green"


# ---------------------------------------------------------------------------
# Portfolio & project summaries (budget vs actuals)
# ---------------------------------------------------------------------------
def portfolio_summary(df):
    """One row per project: budget, actual, variance, RAG, top risk.

    Uses CO project-level totals from df.attrs to compute adjusted figures.
    """
    co_by_project = df.attrs.get("co_by_project", {})
    has_co = bool(co_by_project)
    rows = []
    for name, grp in df.groupby("project_name"):
        budget = grp["budgeted_amount"].sum()
        actual = grp["actual_amount"].sum()
        var = actual - budget
        var_pct = var / budget if budget else 0
        worst = grp.loc[grp["variance"].idxmax()]
        row = {
            "Project": name,
            "Budget": budget,
            "Actual": actual,
            "Variance": var,
            "Variance %": var_pct,
            "Status": assign_rag(var_pct),
            "Top Risk": worst["line_item"],
            "Top Risk $": worst["variance"],
        }
        if has_co:
            co_total = co_by_project.get(name, 0)
            adj_budget = budget + co_total
            adj_var = actual - adj_budget
            adj_pct = adj_var / adj_budget if adj_budget else 0
            row["CO Approved"] = co_total
            row["Adjusted Budget"] = adj_budget
            row["Adjusted Variance"] = adj_var
            row["Adjusted Variance %"] = adj_pct
            row["Adjusted Status"] = assign_rag(adj_pct)
        rows.append(row)
    return pd.DataFrame(rows)


def phase_summary(df, project):
    """Group by phase for a single project."""
    grp = df[df["project_name"] == project].groupby("phase").agg(
        Budget=("budgeted_amount", "sum"),
        Actual=("actual_amount", "sum"),
    ).reset_index()
    grp["Variance"] = grp["Actual"] - grp["Budget"]
    grp["Variance %"] = grp["Variance"] / grp["Budget"]
    grp["Status"] = grp["Variance %"].apply(assign_rag)
    return grp.rename(columns={"phase": "Phase"})


def category_summary(df, project):
    """Group by cost category for a single project."""
    grp = df[df["project_name"] == project].groupby("cost_category").agg(
        Budget=("budgeted_amount", "sum"),
        Actual=("actual_amount", "sum"),
    ).reset_index()
    grp["Variance"] = grp["Actual"] - grp["Budget"]
    grp["Variance %"] = grp["Variance"] / grp["Budget"]
    grp["Status"] = grp["Variance %"].apply(assign_rag)
    return grp.rename(columns={"cost_category": "Category"})


def top_risks(df, n=5, project=None):
    """Top N line items by dollar variance (highest overrun first)."""
    subset = df if project is None else df[df["project_name"] == project]
    return (subset.nlargest(n, "variance")
            [["project_name", "phase", "line_item", "budgeted_amount",
              "actual_amount", "variance", "variance_pct"]]
            .rename(columns={
                "project_name": "Project",
                "phase": "Phase",
                "line_item": "Line Item",
                "budgeted_amount": "Budget",
                "actual_amount": "Actual",
                "variance": "Variance",
                "variance_pct": "Variance %",
            }))


def run_outlier_detection(df, project=None):
    """Run outlier detection on merged data. Optionally filter to one project."""
    subset = df if project is None else df[df["project_name"] == project]
    flags = detect_outliers(subset)
    summary = outlier_summary(flags)
    by_proj = outlier_by_project(flags)
    by_cat = outlier_by_category(flags)
    return flags, summary, by_proj, by_cat


# ---------------------------------------------------------------------------
# Change Order Analysis
# ---------------------------------------------------------------------------
def change_order_summary(co_df, project=None):
    """Summarize change orders by project. Returns (summary_df, totals_dict)."""
    df = co_df.copy()
    if project:
        df = df[df["project_name"] == project]
    if df.empty:
        return pd.DataFrame(), {"total_cos": 0, "total_impact": 0, "approved_impact": 0, "pending_impact": 0}

    df["cost_impact"] = pd.to_numeric(df["cost_impact"], errors="coerce").fillna(0)

    has_status = "status" in df.columns
    if has_status:
        status_lower = df["status"].str.lower().str.strip()
        approved_mask = status_lower == "approved"
        pending_mask = status_lower == "pending"
    else:
        approved_mask = pd.Series(True, index=df.index)
        pending_mask = pd.Series(False, index=df.index)

    totals = {
        "total_cos": len(df),
        "total_impact": df["cost_impact"].sum(),
        "approved_impact": df.loc[approved_mask, "cost_impact"].sum(),
        "pending_impact": df.loc[pending_mask, "cost_impact"].sum(),
        "approved_count": approved_mask.sum(),
        "pending_count": pending_mask.sum(),
    }

    # Per-project summary
    rows = []
    for name, grp in df.groupby("project_name"):
        g_approved = grp.loc[grp.index.isin(df[approved_mask].index)]
        g_pending = grp.loc[grp.index.isin(df[pending_mask].index)]
        rows.append({
            "Project": name,
            "Total COs": len(grp),
            "Approved": len(g_approved),
            "Pending": len(g_pending),
            "Approved $": g_approved["cost_impact"].sum(),
            "Pending $": g_pending["cost_impact"].sum(),
            "Total Impact": grp["cost_impact"].sum(),
        })

    return pd.DataFrame(rows), totals


# ---------------------------------------------------------------------------
# Schedule Analysis
# ---------------------------------------------------------------------------
def schedule_alerts(schedule_df, project=None, slip_threshold_days=5):
    """Identify tasks that are slipping or at risk.

    Returns (alerts_df, stats_dict).
    """
    df = schedule_df.copy()
    if project:
        df = df[df["project_name"] == project]
    if df.empty:
        return pd.DataFrame(), {"total_tasks": 0, "slipping": 0, "at_risk": 0, "on_track": 0, "complete": 0}

    alerts = []
    today = pd.Timestamp.now().normalize()

    for _, row in df.iterrows():
        task = {
            "Project": row["project_name"],
            "Task": row.get("task_name", ""),
            "Phase": row.get("phase", ""),
            "Planned Start": row.get("planned_start"),
            "Planned End": row.get("planned_end"),
            "% Complete": row.get("pct_complete", 0),
            "Status": "On Track",
            "Slip Days": 0,
            "Risk Level": "green",
        }

        pct = row.get("pct_complete", 0) or 0

        # Completed tasks
        if pct >= 100:
            end_slip = row.get("end_slip_days")
            if pd.notna(end_slip) and end_slip > 0:
                task["Status"] = f"Completed {int(end_slip)}d late"
                task["Slip Days"] = int(end_slip)
                task["Risk Level"] = "yellow"
            else:
                task["Status"] = "Complete"
            alerts.append(task)
            continue

        # In-progress: check projected slippage
        projected_slip = row.get("projected_slip_days")
        start_slip = row.get("start_slip_days", 0) or 0

        if pd.notna(projected_slip) and projected_slip > slip_threshold_days:
            task["Status"] = f"Slipping — {int(projected_slip)}d projected delay"
            task["Slip Days"] = int(projected_slip)
            task["Risk Level"] = "red" if projected_slip > slip_threshold_days * 2 else "yellow"
        elif start_slip > slip_threshold_days:
            task["Status"] = f"Late start — {int(start_slip)}d behind"
            task["Slip Days"] = int(start_slip)
            task["Risk Level"] = "yellow"
        elif pd.notna(row.get("planned_end")) and row["planned_end"] < today and pct < 100:
            overdue = (today - row["planned_end"]).days
            task["Status"] = f"Overdue — {overdue}d past planned end"
            task["Slip Days"] = overdue
            task["Risk Level"] = "red"

        alerts.append(task)

    alerts_df = pd.DataFrame(alerts)

    stats = {
        "total_tasks": len(alerts_df),
        "slipping": len(alerts_df[alerts_df["Risk Level"] == "red"]),
        "at_risk": len(alerts_df[alerts_df["Risk Level"] == "yellow"]),
        "on_track": len(alerts_df[alerts_df["Risk Level"] == "green"]),
        "complete": len(alerts_df[alerts_df["% Complete"] >= 100]) if "% Complete" in alerts_df.columns else 0,
    }

    # Sort: red first, then yellow, then green
    risk_order = {"red": 0, "yellow": 1, "green": 2}
    alerts_df["_sort"] = alerts_df["Risk Level"].map(risk_order)
    alerts_df = alerts_df.sort_values("_sort").drop(columns="_sort")

    return alerts_df, stats


# ---------------------------------------------------------------------------
# Labor Productivity Analysis
# ---------------------------------------------------------------------------
def labor_productivity(timecards_df, budget_df=None, project=None):
    """Analyze labor productivity from timecard data.

    Returns (summary_df, stats_dict).
    """
    df = timecards_df.copy()
    if project:
        df = df[df["project_name"] == project]
    if df.empty:
        return pd.DataFrame(), {"total_hours": 0, "total_cost": 0, "avg_rate": 0, "overtime_pct": 0}

    has_rate = "hourly_rate" in df.columns and df["hourly_rate"].notna().any()
    has_ot = "overtime_hours" in df.columns

    total_hours = df["hours"].sum()
    total_ot = df["overtime_hours"].sum() if has_ot else 0
    total_cost = df["labor_cost"].sum() if "labor_cost" in df.columns else 0
    avg_rate = (total_cost / total_hours) if total_hours > 0 else 0
    ot_pct = (total_ot / total_hours * 100) if total_hours > 0 else 0

    stats = {
        "total_hours": total_hours,
        "total_cost": total_cost,
        "avg_rate": avg_rate,
        "overtime_pct": ot_pct,
        "overtime_hours": total_ot,
        "unique_workers": df["worker_name"].nunique() if "worker_name" in df.columns else 0,
    }

    # Per-project or per-phase breakdown
    group_col = "phase" if project else "project_name"
    if group_col not in df.columns:
        return pd.DataFrame(), stats

    rows = []
    for name, grp in df.groupby(group_col):
        hrs = grp["hours"].sum()
        ot = grp["overtime_hours"].sum() if has_ot else 0
        cost = grp["labor_cost"].sum() if "labor_cost" in grp.columns else 0
        workers = grp["worker_name"].nunique() if "worker_name" in grp.columns else 0
        row = {
            "Group": name,
            "Hours": hrs,
            "Overtime": ot,
            "OT %": (ot / hrs * 100) if hrs > 0 else 0,
            "Workers": workers,
        }
        if has_rate:
            row["Labor Cost"] = cost
            row["Avg Rate"] = cost / hrs if hrs > 0 else 0
        rows.append(row)

    summary_df = pd.DataFrame(rows)
    if has_rate:
        summary_df = summary_df.sort_values("Labor Cost", ascending=False)

    # Crew-level analysis
    if "crew" in df.columns:
        crew_rows = []
        for name, grp in df.groupby("crew"):
            hrs = grp["hours"].sum()
            ot = grp["overtime_hours"].sum() if has_ot else 0
            cost = grp["labor_cost"].sum() if "labor_cost" in grp.columns else 0
            workers = grp["worker_name"].nunique()
            days = grp["date"].nunique() if "date" in grp.columns else 1
            crew_rows.append({
                "Crew": name,
                "Workers": workers,
                "Total Hours": hrs,
                "Hours/Day": hrs / days if days > 0 else 0,
                "Overtime": ot,
                "OT %": (ot / hrs * 100) if hrs > 0 else 0,
                "Labor Cost": cost,
            })
        stats["crew_summary"] = pd.DataFrame(crew_rows)

    return summary_df, stats


# ---------------------------------------------------------------------------
# Material Delivery Risk Analysis
# ---------------------------------------------------------------------------
def material_risk_summary(materials_df, project=None):
    """Analyze material delivery risk.

    Returns (summary_df, stats_dict).
    """
    df = materials_df.copy()
    if project:
        df = df[df["project_name"] == project]
    if df.empty:
        return pd.DataFrame(), {"total_orders": 0, "total_value": 0, "at_risk": 0, "delivered": 0}

    total_value = df["total_cost"].sum() if "total_cost" in df.columns else 0
    has_risk = "delivery_risk" in df.columns
    has_status = "status" in df.columns

    stats = {
        "total_orders": len(df),
        "total_value": total_value,
    }

    if has_status:
        status_lower = df["status"].str.lower().str.strip()
        stats["delivered"] = (status_lower == "delivered").sum()
        stats["ordered"] = (status_lower == "ordered").sum()
        stats["in_transit"] = (status_lower == "in transit").sum()
        stats["backordered"] = (status_lower == "backordered").sum()

    if has_risk:
        stats["high_risk"] = (df["delivery_risk"] == "High Risk").sum()
        stats["overdue"] = (df["delivery_risk"] == "Overdue").sum()
        stats["watch"] = (df["delivery_risk"] == "Watch").sum()
        stats["at_risk"] = stats["high_risk"] + stats["overdue"] + stats["watch"]
        at_risk_value = df.loc[
            df["delivery_risk"].isin(["High Risk", "Overdue", "Watch"]), "total_cost"
        ].sum()
        stats["at_risk_value"] = at_risk_value

    # Build display table
    display_cols = ["project_name", "material", "phase", "vendor", "status",
                    "order_date", "delivery_date", "total_cost", "delivery_risk"]
    available = [c for c in display_cols if c in df.columns]
    summary_df = df[available].copy()

    # Sort: high risk first
    if has_risk:
        risk_order = {"Overdue": 0, "High Risk": 1, "Watch": 2, "On Track": 3}
        summary_df["_sort"] = summary_df["delivery_risk"].map(risk_order).fillna(4)
        summary_df = summary_df.sort_values("_sort").drop(columns="_sort")

    rename = {
        "project_name": "Project",
        "material": "Material",
        "phase": "Phase",
        "vendor": "Vendor",
        "status": "Status",
        "order_date": "Ordered",
        "delivery_date": "Delivery",
        "total_cost": "Value",
        "delivery_risk": "Risk",
    }
    summary_df = summary_df.rename(columns={k: v for k, v in rename.items() if k in summary_df.columns})

    return summary_df, stats


# ---------------------------------------------------------------------------
# Project Health Score (0–100)
# ---------------------------------------------------------------------------
def project_health_score(project_name, df, co_df=None, schedule_df=None,
                         timecards_df=None, materials_df=None):
    """Composite health score for a single project.

    Returns dict with 'score', 'grade', 'color', 'factors' (list of
    {name, score, weight, detail} dicts).
    """
    factors = []

    # --- 1. Budget variance (weight: 35) ---
    proj_rows = df[df["project_name"] == project_name]
    if not proj_rows.empty:
        budget = proj_rows["budgeted_amount"].sum()
        actual = proj_rows["actual_amount"].sum()
        var_pct = (actual - budget) / budget if budget else 0
        # 0% overrun = 100, 5% = 75, 10% = 50, 20% = 0
        budget_score = max(0, min(100, 100 - (var_pct * 500)))
        factors.append({
            "name": "Budget Variance",
            "score": round(budget_score),
            "weight": 35,
            "detail": f"{var_pct:+.1%} variance (${actual - budget:+,.0f})",
        })
    else:
        factors.append({"name": "Budget Variance", "score": 50, "weight": 35,
                        "detail": "No budget data"})

    # --- 2. Change order exposure (weight: 15) ---
    if co_df is not None and not co_df.empty:
        proj_co = co_df[co_df["project_name"] == project_name]
        if not proj_co.empty and not proj_rows.empty:
            budget = proj_rows["budgeted_amount"].sum()
            co_total = pd.to_numeric(proj_co["cost_impact"], errors="coerce").fillna(0).sum()
            co_pct = abs(co_total) / budget if budget else 0
            # 0% = 100, 5% = 75, 15% = 25, 20%+ = 0
            co_score = max(0, min(100, 100 - (co_pct * 500)))
            factors.append({
                "name": "Change Orders",
                "score": round(co_score),
                "weight": 15,
                "detail": f"{len(proj_co)} COs totaling ${co_total:,.0f} ({co_pct:.1%} of budget)",
            })
        else:
            factors.append({"name": "Change Orders", "score": 100, "weight": 15,
                            "detail": "No change orders — clean scope"})
    else:
        factors.append({"name": "Change Orders", "score": 100, "weight": 15,
                        "detail": "No change orders — clean scope"})

    # --- 3. Schedule performance (weight: 20) ---
    if schedule_df is not None and not schedule_df.empty:
        proj_sched = schedule_df[schedule_df["project_name"] == project_name]
        if not proj_sched.empty:
            total_tasks = len(proj_sched)
            today = pd.Timestamp.now().normalize()
            overdue = 0
            slipping = 0
            for _, row in proj_sched.iterrows():
                pct = row.get("pct_complete", 0) or 0
                if pct >= 100:
                    continue
                planned_end = row.get("planned_end")
                if pd.notna(planned_end) and planned_end < today:
                    overdue += 1
                proj_slip = row.get("projected_slip_days")
                if pd.notna(proj_slip) and proj_slip > 5:
                    slipping += 1
            problem_pct = (overdue + slipping) / total_tasks if total_tasks else 0
            sched_score = max(0, min(100, 100 - (problem_pct * 200)))
            if overdue > 0:
                detail = f"{overdue} overdue, {slipping} slipping of {total_tasks} tasks"
            elif slipping > 0:
                detail = f"{slipping} slipping of {total_tasks} tasks"
            else:
                detail = f"All {total_tasks} tasks on track"
            factors.append({
                "name": "Schedule",
                "score": round(sched_score),
                "weight": 20,
                "detail": detail,
            })
        else:
            factors.append({"name": "Schedule", "score": 75, "weight": 20,
                            "detail": "No schedule data for this project"})
    else:
        factors.append({"name": "Schedule", "score": 75, "weight": 20,
                        "detail": "No schedule data available"})

    # --- 4. Labor / overtime (weight: 15) ---
    if timecards_df is not None and not timecards_df.empty:
        proj_tc = timecards_df[timecards_df["project_name"] == project_name]
        if not proj_tc.empty:
            total_hrs = proj_tc["hours"].sum()
            ot_hrs = proj_tc["overtime_hours"].sum() if "overtime_hours" in proj_tc.columns else 0
            ot_pct = (ot_hrs / total_hrs * 100) if total_hrs > 0 else 0
            # 0% OT = 100, 10% = 80, 25% = 50, 50%+ = 0
            labor_score = max(0, min(100, 100 - (ot_pct * 2)))
            factors.append({
                "name": "Labor",
                "score": round(labor_score),
                "weight": 15,
                "detail": f"{ot_pct:.1f}% overtime ({ot_hrs:,.0f} of {total_hrs:,.0f} hours)",
            })
        else:
            factors.append({"name": "Labor", "score": 75, "weight": 15,
                            "detail": "No timecard data for this project"})
    else:
        factors.append({"name": "Labor", "score": 75, "weight": 15,
                        "detail": "No timecard data available"})

    # --- 5. Material delivery risk (weight: 10) ---
    if materials_df is not None and not materials_df.empty:
        proj_mat = materials_df[materials_df["project_name"] == project_name]
        if not proj_mat.empty:
            total_orders = len(proj_mat)
            at_risk = 0
            if "delivery_risk" in proj_mat.columns:
                at_risk = proj_mat["delivery_risk"].isin(["Overdue", "High Risk", "Watch"]).sum()
            risk_pct = at_risk / total_orders if total_orders else 0
            mat_score = max(0, min(100, 100 - (risk_pct * 200)))
            if at_risk > 0:
                detail = f"{at_risk} of {total_orders} orders at risk"
            else:
                detail = f"All {total_orders} orders on track"
            factors.append({
                "name": "Materials",
                "score": round(mat_score),
                "weight": 10,
                "detail": detail,
            })
        else:
            factors.append({"name": "Materials", "score": 75, "weight": 10,
                            "detail": "No material data for this project"})
    else:
        factors.append({"name": "Materials", "score": 75, "weight": 10,
                        "detail": "No material data available"})

    # --- 6. Outlier flags (weight: 5) ---
    if not proj_rows.empty:
        flags = detect_outliers(proj_rows)
        n_flags = len(flags)
        n_items = len(proj_rows)
        flag_pct = n_flags / n_items if n_items else 0
        outlier_score = max(0, min(100, 100 - (flag_pct * 300)))
        if n_flags > 0:
            detail = f"{n_flags} anomalous line items of {n_items}"
        else:
            detail = "No anomalies detected"
        factors.append({
            "name": "Outliers",
            "score": round(outlier_score),
            "weight": 5,
            "detail": detail,
        })
    else:
        factors.append({"name": "Outliers", "score": 75, "weight": 5,
                        "detail": "No data to analyze"})

    # --- Weighted composite ---
    total_weight = sum(f["weight"] for f in factors)
    score = sum(f["score"] * f["weight"] for f in factors) / total_weight if total_weight else 0
    score = round(score)

    if score >= 85:
        grade, color = "Healthy", "#22c55e"
    elif score >= 70:
        grade, color = "Watch", "#f59e0b"
    elif score >= 50:
        grade, color = "At Risk", "#f97316"
    else:
        grade, color = "Critical", "#ef4444"

    return {"score": score, "grade": grade, "color": color, "factors": factors}


# ---------------------------------------------------------------------------
# Data Quality Score (0–100)
# ---------------------------------------------------------------------------
def data_quality_score(project_name, df, co_df=None, schedule_df=None,
                       timecards_df=None, materials_df=None):
    """Assess how complete and reliable the data is for a project.

    Returns dict with 'score', 'grade', 'color', 'reasons' (list of
    {message, impact, severity} dicts).
    """
    reasons = []
    points = 100  # Start at 100, deduct for issues

    proj_rows = df[df["project_name"] == project_name]

    # --- 1. Budget/actuals completeness ---
    if proj_rows.empty:
        points -= 40
        reasons.append({"message": "No budget or actuals data found",
                        "impact": -40, "severity": "critical"})
    else:
        n_rows = len(proj_rows)
        zero_budget = (proj_rows["budgeted_amount"] == 0).sum()
        zero_actual = (proj_rows["actual_amount"] == 0).sum()

        if zero_budget > 0:
            pct = zero_budget / n_rows * 100
            deduction = min(15, round(pct / 5))
            points -= deduction
            reasons.append({
                "message": f"{zero_budget} of {n_rows} line items have $0 budget",
                "impact": -deduction, "severity": "warning"})

        if zero_actual > n_rows * 0.8:
            points -= 10
            reasons.append({
                "message": f"{zero_actual} of {n_rows} line items have $0 actuals — data may be incomplete",
                "impact": -10, "severity": "warning"})

        # Check for reasonable number of line items
        if n_rows < 5:
            points -= 10
            reasons.append({
                "message": f"Only {n_rows} line items — unusually low detail for a project",
                "impact": -10, "severity": "warning"})

        # Check for missing phases or categories
        missing_phase = proj_rows["phase"].isna().sum() + (proj_rows["phase"] == "").sum()
        if missing_phase > 0:
            points -= 5
            reasons.append({
                "message": f"{missing_phase} line items missing phase classification",
                "impact": -5, "severity": "info"})

        missing_cat = proj_rows["cost_category"].isna().sum() + (proj_rows["cost_category"] == "").sum()
        if missing_cat > 0:
            points -= 5
            reasons.append({
                "message": f"{missing_cat} line items missing cost category",
                "impact": -5, "severity": "info"})

    # --- 2. Change order data ---
    if co_df is not None and not co_df.empty:
        proj_co = co_df[co_df["project_name"] == project_name]
        if not proj_co.empty:
            missing_status = proj_co["status"].isna().sum() if "status" in proj_co.columns else len(proj_co)
            if missing_status > 0:
                points -= 5
                reasons.append({
                    "message": f"{missing_status} change orders missing approval status",
                    "impact": -5, "severity": "warning"})
        # Having COs is fine, not having them just means no deduction
    else:
        points -= 5
        reasons.append({
            "message": "No change order data — cannot separate scope changes from true overruns",
            "impact": -5, "severity": "info"})

    # --- 3. Schedule data ---
    if schedule_df is not None and not schedule_df.empty:
        proj_sched = schedule_df[schedule_df["project_name"] == project_name]
        if not proj_sched.empty:
            missing_pct = 0
            if "pct_complete" in proj_sched.columns:
                missing_pct = proj_sched["pct_complete"].isna().sum()
            else:
                missing_pct = len(proj_sched)
            if missing_pct > 0:
                deduction = min(8, round(missing_pct / len(proj_sched) * 8))
                points -= deduction
                reasons.append({
                    "message": f"{missing_pct} of {len(proj_sched)} tasks missing % complete — schedule tracking is blind",
                    "impact": -deduction, "severity": "warning"})

            missing_actual_start = 0
            if "actual_start" in proj_sched.columns:
                missing_actual_start = proj_sched["actual_start"].isna().sum()
            else:
                missing_actual_start = len(proj_sched)
            if missing_actual_start > len(proj_sched) * 0.5:
                points -= 5
                reasons.append({
                    "message": f"{missing_actual_start} tasks missing actual start date",
                    "impact": -5, "severity": "info"})
        else:
            points -= 10
            reasons.append({
                "message": "No schedule data for this project — cannot track timeline risk",
                "impact": -10, "severity": "warning"})
    else:
        points -= 10
        reasons.append({
            "message": "No schedule data uploaded — timeline risk is invisible",
            "impact": -10, "severity": "warning"})

    # --- 4. Timecard / labor data ---
    if timecards_df is not None and not timecards_df.empty:
        proj_tc = timecards_df[timecards_df["project_name"] == project_name]
        if not proj_tc.empty:
            if "hourly_rate" not in proj_tc.columns or proj_tc["hourly_rate"].isna().all():
                points -= 5
                reasons.append({
                    "message": "Timecards missing hourly rates — cannot calculate labor cost",
                    "impact": -5, "severity": "info"})

            # Check date coverage — are there recent entries?
            if "date" in proj_tc.columns:
                latest = proj_tc["date"].max()
                if pd.notna(latest):
                    days_since = (pd.Timestamp.now() - latest).days
                    if days_since > 14:
                        points -= 8
                        reasons.append({
                            "message": f"Most recent timecard is {days_since} days old — labor data may be stale",
                            "impact": -8, "severity": "warning"})
        else:
            points -= 10
            reasons.append({
                "message": "No timecard data for this project — labor productivity unknown",
                "impact": -10, "severity": "warning"})
    else:
        points -= 10
        reasons.append({
            "message": "No timecard data uploaded — labor costs are a blind spot",
            "impact": -10, "severity": "warning"})

    # --- 5. Material data ---
    if materials_df is not None and not materials_df.empty:
        proj_mat = materials_df[materials_df["project_name"] == project_name]
        if not proj_mat.empty:
            if "delivery_date" not in proj_mat.columns or proj_mat["delivery_date"].isna().all():
                points -= 5
                reasons.append({
                    "message": "Material orders missing delivery dates — cannot assess delivery risk",
                    "impact": -5, "severity": "info"})
            if "vendor" not in proj_mat.columns or proj_mat["vendor"].isna().all():
                points -= 3
                reasons.append({
                    "message": "Material orders missing vendor info",
                    "impact": -3, "severity": "info"})
        else:
            points -= 8
            reasons.append({
                "message": "No material data for this project — delivery risk untracked",
                "impact": -8, "severity": "info"})
    else:
        points -= 8
        reasons.append({
            "message": "No material data uploaded — supply chain risk is invisible",
            "impact": -8, "severity": "info"})

    # --- Finalize ---
    score = max(0, min(100, points))

    if score >= 85:
        grade, color = "Excellent", "#22c55e"
    elif score >= 70:
        grade, color = "Good", "#3b82f6"
    elif score >= 50:
        grade, color = "Fair", "#f59e0b"
    else:
        grade, color = "Poor", "#ef4444"

    # Add positive note if score is high
    if not reasons:
        reasons.append({"message": "All data sources complete and well-formed",
                        "impact": 0, "severity": "success"})

    return {"score": score, "grade": grade, "color": color, "reasons": reasons}
