"""Outlier detection engine for BMM Project Optimizer.

Detects anomalous line items using three methods:
1. IQR (Interquartile Range) - flags values outside 1.5x IQR fences
2. Z-score - flags values beyond configurable standard deviations
3. Peer comparison - compares line items against same phase/category peers

Returns flagged items with severity, method, and estimated dollar impact.
"""
import pandas as pd
import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
Z_THRESHOLD = 2.0          # standard deviations for z-score method
IQR_MULTIPLIER = 1.5       # multiplier for IQR fences
PEER_MIN_GROUP = 3          # minimum peers needed for peer comparison
SEVERITY_THRESHOLDS = {
    "critical": 0.25,       # 25%+ over budget
    "high": 0.15,           # 15-25% over budget
    "medium": 0.08,         # 8-15% over budget
}


# ---------------------------------------------------------------------------
# Core detection methods
# ---------------------------------------------------------------------------

def _iqr_outliers(series: pd.Series) -> pd.Series:
    """Return boolean mask of values outside IQR fences (upper only - overruns)."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    upper_fence = q3 + IQR_MULTIPLIER * iqr
    return series > upper_fence


def _zscore_outliers(series: pd.Series, threshold: float = Z_THRESHOLD) -> pd.Series:
    """Return boolean mask of values with z-score above threshold."""
    if series.std() == 0:
        return pd.Series(False, index=series.index)
    z = (series - series.mean()) / series.std()
    return z > threshold


def _assign_severity(variance_pct: float) -> str:
    """Assign severity based on variance percentage."""
    if variance_pct >= SEVERITY_THRESHOLDS["critical"]:
        return "critical"
    elif variance_pct >= SEVERITY_THRESHOLDS["high"]:
        return "high"
    elif variance_pct >= SEVERITY_THRESHOLDS["medium"]:
        return "medium"
    return "low"


# ---------------------------------------------------------------------------
# Main detection functions
# ---------------------------------------------------------------------------

def detect_outliers(df: pd.DataFrame, methods: Optional[list] = None) -> pd.DataFrame:
    """Run outlier detection on a merged budget/actuals dataframe.

    Parameters
    ----------
    df : DataFrame with columns: project_name, phase, cost_category, line_item,
         budgeted_amount, actual_amount, variance, variance_pct
    methods : list of methods to use, default ["iqr", "zscore", "peer"]

    Returns
    -------
    DataFrame of flagged line items with columns:
        project_name, phase, cost_category, line_item,
        budgeted_amount, actual_amount, variance, variance_pct,
        severity, detection_method, peer_avg_variance_pct, dollar_impact
    """
    if methods is None:
        methods = ["iqr", "zscore", "peer"]

    # Only look at items that are over budget
    over = df[df["variance"] > 0].copy()
    if over.empty:
        return _empty_result()

    flagged = []

    # Method 1: IQR on variance_pct across all line items
    if "iqr" in methods and len(over) >= 4:
        iqr_mask = _iqr_outliers(over["variance_pct"])
        for idx in over[iqr_mask].index:
            row = over.loc[idx]
            flagged.append(_build_flag(row, "iqr"))

    # Method 2: Z-score on variance_pct across all line items
    if "zscore" in methods and len(over) >= 4:
        z_mask = _zscore_outliers(over["variance_pct"])
        for idx in over[z_mask].index:
            row = over.loc[idx]
            flagged.append(_build_flag(row, "zscore"))

    # Method 3: Peer comparison - compare within same phase + cost_category
    if "peer" in methods:
        peer_flags = _peer_comparison(over)
        flagged.extend(peer_flags)

    if not flagged:
        return _empty_result()

    result = pd.DataFrame(flagged)

    # Deduplicate: keep highest severity per line item, combine methods
    result = _deduplicate(result)

    # Sort by dollar impact descending
    result = result.sort_values("dollar_impact", ascending=False).reset_index(drop=True)

    return result


def _peer_comparison(df: pd.DataFrame) -> list:
    """Compare each line item's variance against peers in same phase + category."""
    flags = []
    for (phase, cat), grp in df.groupby(["phase", "cost_category"]):
        if len(grp) < PEER_MIN_GROUP:
            continue
        median_pct = grp["variance_pct"].median()
        std_pct = grp["variance_pct"].std()
        if std_pct == 0:
            continue
        for idx, row in grp.iterrows():
            # Flag if more than 1.5 std above peer median
            if row["variance_pct"] > median_pct + 1.5 * std_pct:
                flag = _build_flag(row, "peer")
                flag["peer_avg_variance_pct"] = median_pct
                flags.append(flag)
    return flags


def _build_flag(row: pd.Series, method: str) -> dict:
    """Build a flag dictionary from a row."""
    vpct = row["variance_pct"]
    return {
        "project_name": row["project_name"],
        "phase": row["phase"],
        "cost_category": row["cost_category"],
        "line_item": row["line_item"],
        "budgeted_amount": row["budgeted_amount"],
        "actual_amount": row["actual_amount"],
        "variance": row["variance"],
        "variance_pct": vpct,
        "severity": _assign_severity(vpct),
        "detection_method": method,
        "peer_avg_variance_pct": None,
        "dollar_impact": row["variance"],
    }


def _deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Deduplicate flags: one row per line item, combine methods, keep worst severity."""
    severity_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    key_cols = ["project_name", "phase", "cost_category", "line_item"]

    deduped = []
    for key, grp in df.groupby(key_cols):
        best = grp.loc[grp["severity"].map(severity_rank).idxmin()]
        methods = sorted(grp["detection_method"].unique())
        row = best.to_dict()
        row["detection_method"] = " + ".join(methods)
        # Use peer avg if available from any method
        peer_vals = grp["peer_avg_variance_pct"].dropna()
        if not peer_vals.empty:
            row["peer_avg_variance_pct"] = peer_vals.iloc[0]
        deduped.append(row)

    return pd.DataFrame(deduped)


def _empty_result() -> pd.DataFrame:
    """Return empty DataFrame with expected columns."""
    return pd.DataFrame(columns=[
        "project_name", "phase", "cost_category", "line_item",
        "budgeted_amount", "actual_amount", "variance", "variance_pct",
        "severity", "detection_method", "peer_avg_variance_pct", "dollar_impact",
    ])


# ---------------------------------------------------------------------------
# Summary / rollup functions
# ---------------------------------------------------------------------------

def outlier_summary(flags: pd.DataFrame) -> dict:
    """Compute summary stats from flagged outliers."""
    if flags.empty:
        return {
            "total_flags": 0,
            "total_dollar_impact": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "top_project": None,
            "top_category": None,
        }

    by_sev = flags["severity"].value_counts()
    by_project = flags.groupby("project_name")["dollar_impact"].sum()
    by_cat = flags.groupby("cost_category")["dollar_impact"].sum()

    return {
        "total_flags": len(flags),
        "total_dollar_impact": flags["dollar_impact"].sum(),
        "critical": int(by_sev.get("critical", 0)),
        "high": int(by_sev.get("high", 0)),
        "medium": int(by_sev.get("medium", 0)),
        "low": int(by_sev.get("low", 0)),
        "top_project": by_project.idxmax() if not by_project.empty else None,
        "top_category": by_cat.idxmax() if not by_cat.empty else None,
    }


def outlier_by_project(flags: pd.DataFrame) -> pd.DataFrame:
    """Rollup: flags and dollar impact per project."""
    if flags.empty:
        return pd.DataFrame(columns=["project_name", "flags", "dollar_impact", "worst_severity"])

    severity_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}

    rows = []
    for name, grp in flags.groupby("project_name"):
        worst = grp["severity"].map(severity_rank).min()
        worst_label = {v: k for k, v in severity_rank.items()}[worst]
        rows.append({
            "project_name": name,
            "flags": len(grp),
            "dollar_impact": grp["dollar_impact"].sum(),
            "worst_severity": worst_label,
        })
    return pd.DataFrame(rows).sort_values("dollar_impact", ascending=False).reset_index(drop=True)


def outlier_by_category(flags: pd.DataFrame) -> pd.DataFrame:
    """Rollup: flags and dollar impact per cost category."""
    if flags.empty:
        return pd.DataFrame(columns=["cost_category", "flags", "dollar_impact"])

    return (flags.groupby("cost_category")
            .agg(flags=("line_item", "count"), dollar_impact=("dollar_impact", "sum"))
            .sort_values("dollar_impact", ascending=False)
            .reset_index())
