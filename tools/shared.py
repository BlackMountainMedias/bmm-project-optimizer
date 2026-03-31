"""Shared state, theme, and data loading for multi-page dashboard."""
import os
import streamlit as st
import pandas as pd
from functools import partial
from data_loader import (load_sample_data, merge_budget_actuals, parse_schedule,
                         parse_timecards, parse_materials, BUDGET_COLS, ACTUALS_COLS)
from calculations import assign_rag

LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")

RAG_COLORS = {"green": "#22c55e", "yellow": "#f59e0b", "red": "#ef4444"}
RAG_GLOW = {
    "green": "0 0 20px rgba(34,197,94,0.3)",
    "yellow": "0 0 20px rgba(245,158,11,0.3)",
    "red": "0 0 20px rgba(239,68,68,0.3)",
}

SEVERITY_COLORS = {
    "critical": "#ef4444",
    "high": "#f59e0b",
    "medium": "#3b82f6",
    "low": "#64748b",
}

MAT_RISK_COLORS = {"Overdue": "#ef4444", "High Risk": "#f59e0b", "Watch": "#3b82f6", "On Track": "#22c55e"}
SCHED_COLORS = {"red": "#ef4444", "yellow": "#f59e0b", "green": "#22c55e"}


def apply_theme():
    """Inject the dark premium CSS theme."""
    st.markdown("""
<style>
    /* Global */
    .stApp { background-color: #0a0f1a; }
    [data-testid="stHeader"] { background-color: #0a0f1a; }
    [data-testid="stSidebar"] { background-color: #0d1321; border-right: 1px solid #1e293b; }
    [data-testid="stSidebar"] * { color: #94a3b8 !important; }
    [data-testid="stSidebar"] h1 { color: #f1f5f9 !important; }

    /* Typography */
    h1, h2, h3 { color: #f1f5f9 !important; font-weight: 600 !important; letter-spacing: -0.02em; }
    p, span, label, div { color: #cbd5e1; }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 14px 12px;
        overflow: visible !important;
        min-width: 0;
    }
    [data-testid="stMetric"] > div { overflow: visible !important; }
    [data-testid="stMetric"] > div > div { overflow: visible !important; }
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        white-space: nowrap;
        overflow: visible !important;
    }
    [data-testid="stMetricValue"] {
        color: #f1f5f9 !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: unset !important;
    }
    [data-testid="stMetricDelta"] { font-size: 13px !important; }

    /* Plotly charts */
    .js-plotly-plot .plotly .main-svg { background: transparent !important; }

    /* Dataframes */
    [data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
    .stDataFrame div[data-testid="stDataFrameResizable"] { border: 1px solid #1e293b; border-radius: 12px; }

    /* Dividers */
    hr { border-color: #1e293b !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background: transparent; }
    .stTabs [data-baseweb="tab"] {
        background: #111827; border: 1px solid #1e293b; border-radius: 8px;
        color: #94a3b8; padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: #1e293b !important; border-color: #3b82f6 !important; color: #f1f5f9 !important;
    }

    /* Select box */
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background: #111827; border-color: #1e293b;
    }

    /* Hide streamlit branding */
    #MainMenu, footer { display: none; }

    /* Custom card styles */
    .project-card {
        background: linear-gradient(135deg, #111827 0%, #1a1f2e 100%);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 24px;
        transition: all 0.2s;
    }
    .project-card:hover { border-color: #334155; }
    .card-label { color: #64748b; font-size: 11px; text-transform: uppercase;
        letter-spacing: 0.1em; margin-bottom: 4px; }
    .card-project { color: #f1f5f9; font-size: 16px; font-weight: 600;
        margin-bottom: 14px; line-height: 1.3; }
    .card-number { font-size: 36px; font-weight: 800; line-height: 1; margin-bottom: 8px; }
    .card-detail { color: #64748b; font-size: 13px; line-height: 1.7; }
    .card-detail-value { color: #e2e8f0; font-weight: 500; }
    .card-risk { color: #94a3b8; font-size: 12px; margin-top: 14px;
        padding-top: 14px; border-top: 1px solid #1e293b; line-height: 1.5; }
    .status-dot { display: inline-block; width: 8px; height: 8px;
        border-radius: 50%; margin-right: 6px; }
    .risk-row {
        background: #111827;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .risk-label { color: #cbd5e1; font-size: 13px; }
    .risk-project { color: #64748b; font-size: 11px; margin-top: 2px; }
    .risk-amount { font-size: 16px; font-weight: 700; }

    /* Section headers */
    .section-header {
        color: #f1f5f9;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid #1e293b;
    }

    /* Sidebar logo - no filter, use mix-blend-mode for dark bg */
    [data-testid="stSidebar"] img {
        filter: invert(1) brightness(2);
        background: transparent !important;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .stApp { padding: 0 !important; }
        [data-testid="stSidebar"] { min-width: 200px !important; }

        /* Stack metric cards vertically */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 8px !important;
        }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 100% !important;
            min-width: 0 !important;
        }
        [data-testid="stMetric"] {
            padding: 10px 10px !important;
            border-radius: 8px !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 16px !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 10px !important;
        }

        /* Project cards */
        .project-card {
            padding: 14px !important;
            border-radius: 10px !important;
        }
        .card-number { font-size: 24px !important; }
        .card-project { font-size: 14px !important; }
        .card-detail { font-size: 11px !important; }

        /* Tables scroll horizontally */
        [data-testid="stDataFrame"] {
            overflow-x: auto !important;
        }

        /* Tabs smaller on mobile */
        .stTabs [data-baseweb="tab"] {
            padding: 6px 12px !important;
            font-size: 12px !important;
        }

        /* Charts responsive */
        .js-plotly-plot { width: 100% !important; }

        /* Section headers */
        .section-header {
            font-size: 11px !important;
            margin-bottom: 12px !important;
            padding-bottom: 8px !important;
        }

        /* Risk rows */
        .risk-row {
            padding: 10px 12px !important;
            flex-direction: column !important;
            gap: 4px !important;
        }
        .risk-amount { font-size: 14px !important; }
    }


    /* Small phones */
    @media (max-width: 480px) {
        [data-testid="stMetricValue"] {
            font-size: 14px !important;
        }
        .card-number { font-size: 20px !important; }
        h1 { font-size: 20px !important; }
        h2 { font-size: 16px !important; }
        h3 { font-size: 14px !important; }
    }
</style>
""", unsafe_allow_html=True)


def demo_callout(icon, text, color="#ff6b35"):
    """Show a guided insight banner for demo mode."""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {color}15 0%, {color}08 100%);
                border-left: 3px solid {color}; border-radius: 8px;
                padding: 12px 16px; margin-bottom: 16px;">
        <span style="font-size: 16px; margin-right: 8px;">{icon}</span>
        <span style="color: #e2e8f0; font-size: 13px;">{text}</span>
    </div>
    """, unsafe_allow_html=True)


def is_demo_mode():
    """Check if dashboard is running on demo/sample data."""
    return not st.session_state.get("use_uploaded_for_dashboard", False)


def load_data():
    """Load and cache all data. Returns dict with all dataframes and thresholds."""
    if "app_data" in st.session_state:
        return st.session_state["app_data"]

    _init_data()
    return st.session_state["app_data"]


def _init_data():
    """Initialize data from demo or uploaded sources."""
    uploaded = st.session_state.get("uploaded_data", {})
    use_uploaded = st.session_state.get("use_uploaded_for_dashboard", False)

    if use_uploaded and "Budget / Bid" in uploaded and "Actuals / Costs" in uploaded:
        budget_df = uploaded["Budget / Bid"]["df"]
        actuals_df = uploaded["Actuals / Costs"]["df"]
        co_df = uploaded.get("Change Orders", {}).get("df")
        schedule_df = uploaded.get("Project Schedule", {}).get("df")
        timecards_df = uploaded.get("Timecards / Timesheets", {}).get("df")
        materials_df = uploaded.get("Material Orders & Deliveries", {}).get("df")
    else:
        _all_data = load_sample_data()
        budget_df = _all_data["budget"]
        actuals_df = _all_data["actuals"]
        co_df = _all_data.get("change_orders")
        schedule_df = _all_data.get("schedule")
        timecards_df = _all_data.get("timecards")
        materials_df = _all_data.get("materials")

    # Parse supplementary data
    if co_df is not None and not co_df.empty:
        co_df["cost_impact"] = pd.to_numeric(co_df["cost_impact"], errors="coerce").fillna(0)
    if schedule_df is not None and not schedule_df.empty:
        schedule_df = parse_schedule(schedule_df)
    if timecards_df is not None and not timecards_df.empty:
        timecards_df = parse_timecards(timecards_df)
    if materials_df is not None and not materials_df.empty:
        materials_df = parse_materials(materials_df)

    df = merge_budget_actuals(budget_df, actuals_df, change_orders_df=co_df)

    st.session_state["app_data"] = {
        "df": df,
        "co_df": co_df,
        "schedule_df": schedule_df,
        "timecards_df": timecards_df,
        "materials_df": materials_df,
    }


def get_thresholds():
    """Get yellow/red thresholds from sidebar, with defaults."""
    return (
        st.session_state.get("yellow_thresh", 0.05),
        st.session_state.get("red_thresh", 0.10),
    )


def get_rag_func():
    """Return a RAG function using current thresholds."""
    yellow, red = get_thresholds()
    return partial(assign_rag, yellow=yellow, red=red)
