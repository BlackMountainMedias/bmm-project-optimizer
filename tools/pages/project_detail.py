"""Project Detail drill-down page."""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from shared import RAG_COLORS, get_rag_func, load_data
from calculations import (phase_summary, category_summary, run_outlier_detection,
                          assign_rag, project_health_score, data_quality_score)
from shared import SEVERITY_COLORS


def render():
    data = st.session_state["app_data"]
    df = data["df"]
    co_df = data["co_df"]
    schedule_df = data["schedule_df"]
    timecards_df = data["timecards_df"]
    materials_df = data["materials_df"]
    _rag = get_rag_func()
    df["status"] = df["variance_pct"].apply(_rag)

    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h1 style="font-size: 28px; margin-bottom: 4px;">Project Detail</h1>
        <p style="color: #64748b; font-size: 14px; margin: 0;">
            Drill into any project for phase, category, and line-item analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    projects = df["project_name"].unique().tolist()
    selected = st.selectbox("Select Project", projects, label_visibility="collapsed")

    proj_df = df[df["project_name"] == selected]
    proj_budget = proj_df["budgeted_amount"].sum()
    proj_actual = proj_df["actual_amount"].sum()
    proj_var = proj_actual - proj_budget
    proj_pct = proj_var / proj_budget if proj_budget else 0
    proj_status = _rag(proj_pct)
    proj_color = RAG_COLORS[proj_status]

    # --- Health + Data Quality scores ---
    health = project_health_score(selected, df, co_df, schedule_df,
                                  timecards_df, materials_df)
    dq = data_quality_score(selected, df, co_df, schedule_df,
                            timecards_df, materials_df)

    # KPI bar — two rows of 3 for readability
    row1 = st.columns(3)
    row1[0].metric("Budget", f"${proj_budget:,.0f}")
    row1[1].metric("Actual", f"${proj_actual:,.0f}")
    row1[2].metric("Variance", f"${proj_var:+,.0f}")

    row2 = st.columns(3)
    row2[0].metric("Status", f"{proj_status.upper()} ({proj_pct:+.1%})")
    row2[1].metric("Health Score", f"{health['score']} — {health['grade']}")
    row2[2].metric("Data Quality", f"{dq['score']} — {dq['grade']}")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Score breakdown section ---
    score_left, score_right = st.columns(2, gap="large")

    with score_left:
        st.markdown('<div class="section-header">Health Score Breakdown</div>', unsafe_allow_html=True)
        for factor in health["factors"]:
            if factor["score"] >= 85:
                fcolor = "#22c55e"
            elif factor["score"] >= 70:
                fcolor = "#f59e0b"
            elif factor["score"] >= 50:
                fcolor = "#f97316"
            else:
                fcolor = "#ef4444"

            bar_width = max(2, factor["score"])
            st.markdown(f"""
            <div style="background: #111827; border: 1px solid #1e293b; border-radius: 10px;
                        padding: 12px 16px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <div style="color: #cbd5e1; font-size: 13px; font-weight: 600;">
                        {factor['name']}
                        <span style="color: #475569; font-size: 11px; font-weight: 400; margin-left: 6px;">
                            wt {factor['weight']}%
                        </span>
                    </div>
                    <div style="font-size: 18px; font-weight: 800; color: {fcolor};">{factor['score']}</div>
                </div>
                <div style="background: #0a0f1a; border-radius: 3px; height: 4px; overflow: hidden; margin-bottom: 6px;">
                    <div style="width: {bar_width}%; height: 100%; background: {fcolor}; border-radius: 3px;"></div>
                </div>
                <div style="color: #64748b; font-size: 11px;">{factor['detail']}</div>
            </div>
            """, unsafe_allow_html=True)

    with score_right:
        st.markdown('<div class="section-header">Data Quality Assessment</div>', unsafe_allow_html=True)

        # Score badge
        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #1e293b; border-radius: 12px;
                    padding: 16px; display: flex; align-items: center; gap: 16px; margin-bottom: 12px;">
            <div style="font-size: 42px; font-weight: 800; color: {dq['color']}; line-height: 1;">
                {dq['score']}
            </div>
            <div>
                <div style="font-size: 16px; font-weight: 600; color: {dq['color']};">{dq['grade']}</div>
                <div style="color: #64748b; font-size: 12px; margin-top: 2px;">
                    {len(dq['reasons'])} finding{'s' if len(dq['reasons']) != 1 else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        sev_colors = {"critical": "#ef4444", "warning": "#f59e0b", "info": "#3b82f6", "success": "#22c55e"}
        sev_labels = {"critical": "CRITICAL", "warning": "WARNING", "info": "INFO", "success": "OK"}

        for reason in dq["reasons"]:
            scolor = sev_colors.get(reason["severity"], "#64748b")
            slabel = sev_labels.get(reason["severity"], "INFO")
            st.markdown(f"""
            <div style="background: #111827; border: 1px solid #1e293b; border-left: 3px solid {scolor};
                        border-radius: 8px; padding: 10px 14px; margin-bottom: 6px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 2px;">
                    <span style="background: {scolor}; color: white; font-size: 9px; font-weight: 700;
                                 padding: 1px 6px; border-radius: 3px;">{slabel}</span>
                    <span style="color: #94a3b8; font-size: 11px;">{reason['impact']:+d} points</span>
                </div>
                <div style="color: #cbd5e1; font-size: 12px;">{reason['message']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Existing tabs ---
    tab_phase, tab_cat, tab_lines, tab_outliers = st.tabs(["By Phase", "By Category", "Line Items", "Outliers"])

    with tab_phase:
        ph = phase_summary(df, selected)
        fig_ph = go.Figure()
        fig_ph.add_trace(go.Bar(y=ph["Phase"], x=ph["Budget"], name="Budget",
                                orientation="h", marker_color="#334155"))
        fig_ph.add_trace(go.Bar(y=ph["Phase"], x=ph["Actual"], name="Actual",
                                orientation="h",
                                marker_color=[RAG_COLORS[s] for s in ph["Status"]]))
        fig_ph.update_layout(
            barmode="group", height=280,
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(orientation="h", y=1.12, font=dict(color="#94a3b8")),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#64748b"), tickformat="$,.0s"),
            yaxis=dict(tickfont=dict(color="#cbd5e1", size=13)),
        )
        st.plotly_chart(fig_ph, use_container_width=True)
        st.dataframe(
            ph.style.format({
                "Budget": "${:,.0f}", "Actual": "${:,.0f}",
                "Variance": "${:+,.0f}", "Variance %": "{:+.1%}",
            }),
            use_container_width=True, hide_index=True,
        )

    with tab_cat:
        cat = category_summary(df, selected)
        fig_cat = go.Figure()
        fig_cat.add_trace(go.Bar(y=cat["Category"], x=cat["Budget"], name="Budget",
                                 orientation="h", marker_color="#334155"))
        fig_cat.add_trace(go.Bar(y=cat["Category"], x=cat["Actual"], name="Actual",
                                 orientation="h",
                                 marker_color=[RAG_COLORS[s] for s in cat["Status"]]))
        fig_cat.update_layout(
            barmode="group", height=240,
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(orientation="h", y=1.12, font=dict(color="#94a3b8")),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#64748b"), tickformat="$,.0s"),
            yaxis=dict(tickfont=dict(color="#cbd5e1", size=13)),
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        st.dataframe(
            cat.style.format({
                "Budget": "${:,.0f}", "Actual": "${:,.0f}",
                "Variance": "${:+,.0f}", "Variance %": "{:+.1%}",
            }),
            use_container_width=True, hide_index=True,
        )

    with tab_lines:
        detail = proj_df[["phase", "cost_category", "line_item", "budgeted_amount",
                           "actual_amount", "variance", "variance_pct", "status"]].copy()
        detail.columns = ["Phase", "Category", "Line Item", "Budget", "Actual",
                           "Variance", "Variance %", "Status"]
        st.dataframe(
            detail.style.format({
                "Budget": "${:,.0f}", "Actual": "${:,.0f}",
                "Variance": "${:+,.0f}", "Variance %": "{:+.1%}",
            }),
            use_container_width=True, hide_index=True, height=500,
        )

    with tab_outliers:
        proj_flags, proj_ol_stats, _, proj_ol_cat = run_outlier_detection(df, project=selected)

        if proj_ol_stats["total_flags"] == 0:
            st.info("No outliers detected for this project.")
        else:
            ol_kcols = st.columns(3)
            ol_kcols[0].metric("Outliers", f"{proj_ol_stats['total_flags']}")
            ol_kcols[1].metric("Dollar Impact", f"${proj_ol_stats['total_dollar_impact']:,.0f}")
            ol_kcols[2].metric("Critical", f"{proj_ol_stats['critical']}")

            st.markdown("<br>", unsafe_allow_html=True)

            ol_detail = proj_flags[["phase", "cost_category", "line_item",
                                     "budgeted_amount", "actual_amount", "variance",
                                     "variance_pct", "severity", "detection_method"]].copy()
            ol_detail.columns = ["Phase", "Category", "Line Item", "Budget", "Actual",
                                  "Variance", "Variance %", "Severity", "Method"]
            st.dataframe(
                ol_detail.style.format({
                    "Budget": "${:,.0f}", "Actual": "${:,.0f}",
                    "Variance": "${:+,.0f}", "Variance %": "{:+.1%}",
                }),
                use_container_width=True, hide_index=True, height=400,
            )


load_data()
render()
