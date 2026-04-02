"""Portfolio Overview page."""
import streamlit as st
import plotly.graph_objects as go
from shared import RAG_COLORS, RAG_GLOW, get_rag_func, load_data, demo_callout, is_demo_mode
from calculations import portfolio_summary, top_risks, project_health_score, data_quality_score


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
    <div style="margin-bottom: 32px;">
        <h1 style="font-size: 32px; margin-bottom: 4px;">Portfolio Overview</h1>
        <p style="color: #64748b; font-size: 14px; margin: 0;">
            Real-time budget intelligence across all active projects
        </p>
    </div>
    """, unsafe_allow_html=True)

    if is_demo_mode():
        demo_callout("☰", "Tap the arrow icon in the top left corner to open the sidebar and navigate between pages. (Note: on mobile, swipe right from the left edge)", "#3b82f6")
        demo_callout("👋", "Live demo with sample data. You're looking at 3 projects -- one is healthy, one looks healthy but is hiding overruns behind change orders, and one is clearly bleeding. Can you spot which is which?")

    psummary = portfolio_summary(df)

    # KPI bar
    total_budget = psummary["Budget"].sum()
    total_actual = psummary["Actual"].sum()
    total_var = total_actual - total_budget
    n_red = (psummary["Status"] == "red").sum()

    kcols = st.columns(4)
    kcols[0].metric("Portfolio Value", f"${total_budget:,.0f}")
    kcols[1].metric("Total Spend", f"${total_actual:,.0f}")
    kcols[2].metric("Total Variance", f"${total_var:+,.0f}")
    kcols[3].metric("Projects", f"{len(psummary)} ({n_red} at risk)")

    # Project cards with health + data quality scores
    st.markdown('<div class="section-header">Active Projects</div>', unsafe_allow_html=True)

    cols = st.columns(len(psummary), gap="large")
    for i, (_, row) in enumerate(psummary.iterrows()):
        with cols[i]:
            proj_name = row["Project"]
            color = RAG_COLORS[row["Status"]]
            glow = RAG_GLOW[row["Status"]]
            util = min(row["Actual"] / row["Budget"] * 100, 100) if row["Budget"] else 0

            health = project_health_score(proj_name, df, co_df, schedule_df,
                                          timecards_df, materials_df)
            dq = data_quality_score(proj_name, df, co_df, schedule_df,
                                    timecards_df, materials_df)

            # Top contributing issue for health
            worst_factor = min(health["factors"], key=lambda f: f["score"])

            # Card header
            st.markdown(f"""
            <div class="project-card" style="border-left: 3px solid {color}; box-shadow: {glow};">
                <div class="card-label">
                    <span class="status-dot" style="background:{color};"></span>
                    {row['Status'].upper()}
                </div>
                <div class="card-project">{proj_name}</div>
            </div>
            """, unsafe_allow_html=True)

            # Health + Data Quality score boxes
            h_col, dq_col = st.columns(2)
            with h_col:
                st.markdown(f"""
                <div style="background: #0a0f1a; border: 1px solid #1e293b; border-radius: 10px;
                            padding: 12px 12px 16px 12px; text-align: center; margin-bottom: 8px;">
                    <div style="font-size: 28px; font-weight: 800; color: {health['color']}; line-height: 1;">
                        {health['score']}
                    </div>
                    <div style="color: #64748b; font-size: 10px; text-transform: uppercase;
                                letter-spacing: 0.08em; margin-top: 4px;">Health</div>
                </div>
                """, unsafe_allow_html=True)
            with dq_col:
                st.markdown(f"""
                <div style="background: #0a0f1a; border: 1px solid #1e293b; border-radius: 10px;
                            padding: 12px 12px 16px 12px; text-align: center; margin-bottom: 8px;">
                    <div style="font-size: 28px; font-weight: 800; color: {dq['color']}; line-height: 1;">
                        {dq['score']}
                    </div>
                    <div style="color: #64748b; font-size: 10px; text-transform: uppercase;
                                letter-spacing: 0.08em; margin-top: 4px;">Data Quality</div>
                </div>
                """, unsafe_allow_html=True)

            # Budget details + progress bar + concern
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #111827 0%, #1a1f2e 100%);
                        border: 1px solid #1e293b; border-radius: 0 0 16px 16px;
                        padding: 16px 24px; margin-top: -16px;">
                <div class="card-detail">
                    Budget: <span class="card-detail-value">${row['Budget']:,.0f}</span><br>
                    Actual: <span class="card-detail-value">${row['Actual']:,.0f}</span><br>
                    Variance: <span style="color:{color}; font-weight:600;">${row['Variance']:+,.0f}</span>
                </div>
                <div style="margin-top: 14px; background: #0a0f1a; border-radius: 4px; height: 6px; overflow: hidden;">
                    <div style="width: {util:.0f}%; height: 100%; background: {color}; border-radius: 4px;"></div>
                </div>
                <div class="card-risk">
                    <span style="color: #64748b; font-size: 11px;">Biggest concern:</span><br>
                    <span style="color: {health['color']}; font-weight: 500; font-size: 12px;">
                        {worst_factor['name']}: {worst_factor['detail']}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Budget vs Actual chart — full width
    st.markdown('<div class="section-header">Budget vs Actual</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=psummary["Project"], x=psummary["Budget"], name="Budget",
        orientation="h", marker_color="#3b82f6", marker_line_width=0,
        text=[f"${v:,.0f}" for v in psummary["Budget"]],
        textposition="auto", textfont=dict(color="#f1f5f9", size=12),
    ))
    fig.add_trace(go.Bar(
        y=psummary["Project"], x=psummary["Actual"], name="Actual",
        orientation="h", marker_color="#f59e0b", marker_line_width=0,
        text=[f"${v:,.0f}" for v in psummary["Actual"]],
        textposition="auto", textfont=dict(color="#f1f5f9", size=12),
    ))
    fig.update_layout(
        barmode="group", height=max(180, len(psummary) * 80),
        margin=dict(l=0, r=20, t=10, b=0),
        legend=dict(orientation="h", y=1.18, font=dict(color="#94a3b8", size=13)),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#64748b", size=12),
                   tickformat="$,.0f"),
        yaxis=dict(tickfont=dict(color="#cbd5e1", size=14), automargin=True),
        bargap=0.25, bargroupgap=0.1,
    )
    config = {"staticPlot": True}
    st.plotly_chart(fig, use_container_width=True, config=config)

    st.markdown("<br>", unsafe_allow_html=True)

    # Two-column: Top risks + Data quality reasons
    mid, right = st.columns(2, gap="large")

    with mid:
        st.markdown('<div class="section-header">Top Risks</div>', unsafe_allow_html=True)
        risk_df = top_risks(df, n=5)
        for _, r in risk_df.iterrows():
            var_pct = r["Variance %"]
            status = _rag(var_pct)
            rcolor = RAG_COLORS[status]
            st.markdown(f"""
            <div class="risk-row">
                <div>
                    <div class="risk-label">{r['Line Item']}</div>
                    <div class="risk-project">{r['Project']} / {r['Phase']}</div>
                </div>
                <div style="text-align: right;">
                    <div class="risk-amount" style="color: {rcolor};">${r['Variance']:+,.0f}</div>
                    <div style="color: #64748b; font-size: 12px;">{var_pct:+.1%}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-header">Data Quality Notes</div>', unsafe_allow_html=True)
        sev_icons = {"critical": "🔴", "warning": "🟡", "info": "🔵", "success": "🟢"}
        for _, row in psummary.iterrows():
            proj_name = row["Project"]
            dq = data_quality_score(proj_name, df, co_df, schedule_df,
                                    timecards_df, materials_df)
            if dq["reasons"]:
                for reason in dq["reasons"][:2]:
                    icon = sev_icons.get(reason["severity"], "🔵")
                    st.markdown(f"""
                    <div style="background: #111827; border: 1px solid #1e293b; border-radius: 8px;
                                padding: 10px 14px; margin-bottom: 6px;">
                        <div style="color: #cbd5e1; font-size: 12px;">
                            {icon} <span style="color: #94a3b8; font-weight: 500;">{proj_name}</span>
                        </div>
                        <div style="color: #64748b; font-size: 11px; margin-top: 2px;">
                            {reason['message']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


load_data()
render()
