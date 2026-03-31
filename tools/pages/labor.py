"""Labor Productivity page."""
import streamlit as st
import plotly.graph_objects as go
from shared import load_data, demo_callout, is_demo_mode
from calculations import labor_productivity


def render():
    data = st.session_state["app_data"]
    timecards_df = data["timecards_df"]

    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h1 style="font-size: 28px; margin-bottom: 4px;">Labor Productivity</h1>
        <p style="color: #64748b; font-size: 14px; margin: 0;">
            Hours, rates, and overtime analysis — detect productivity drops early
        </p>
    </div>
    """, unsafe_allow_html=True)

    if is_demo_mode():
        demo_callout("👷", "Look at Northgate Industrial Park's overtime. Steel Crew A is averaging 10+ hour days with heavy OT -- that's a sign of rework or scheduling problems that are silently eating margin.")

    if timecards_df is None or timecards_df.empty:
        st.info("No timecard data available. Upload timecards or use demo data.")
        return

    labor_df, labor_stats = labor_productivity(timecards_df)

    # KPI rows — two rows of 3 for readability
    row1 = st.columns(3)
    row1[0].metric("Total Hours", f"{labor_stats['total_hours']:,.0f}")
    row1[1].metric("Labor Cost", f"${labor_stats['total_cost']:,.0f}")
    row1[2].metric("Avg Rate", f"${labor_stats['avg_rate']:,.2f}/hr")

    row2 = st.columns(3)
    row2[0].metric("Overtime", f"{labor_stats['overtime_pct']:.1f}%")
    row2[1].metric("Workers", f"{labor_stats['unique_workers']}")
    row2[2].metric("", "")

    st.markdown("<br>", unsafe_allow_html=True)

    # Labor by Project — full width
    st.markdown('<div class="section-header">Labor by Project</div>', unsafe_allow_html=True)
    if not labor_df.empty:
        fmt = {"Hours": "{:,.0f}", "Overtime": "{:,.0f}", "OT %": "{:.1f}%"}
        if "Labor Cost" in labor_df.columns:
            fmt["Labor Cost"] = "${:,.0f}"
            fmt["Avg Rate"] = "${:,.2f}"
        st.dataframe(labor_df.style.format(fmt), use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Crew Breakdown — full width
    st.markdown('<div class="section-header">Crew Breakdown</div>', unsafe_allow_html=True)
    crew_df = labor_stats.get("crew_summary")
    if crew_df is not None and not crew_df.empty:
        crew_fmt = {
            "Total Hours": "{:,.0f}",
            "Hours/Day": "{:.1f}",
            "Overtime": "{:,.0f}",
            "OT %": "{:.1f}%",
            "Labor Cost": "${:,.0f}",
        }
        st.dataframe(crew_df.style.format(crew_fmt), use_container_width=True, hide_index=True)

    # Overtime chart
    if not labor_df.empty and "Overtime" in labor_df.columns:
        st.markdown('<div class="section-header">Hours vs Overtime by Project</div>', unsafe_allow_html=True)
        fig_lb = go.Figure()
        fig_lb.add_trace(go.Bar(
            y=labor_df["Group"], x=labor_df["Hours"], name="Regular Hours",
            orientation="h", marker_color="#334155",
        ))
        fig_lb.add_trace(go.Bar(
            y=labor_df["Group"], x=labor_df["Overtime"], name="Overtime",
            orientation="h", marker_color="#f59e0b",
        ))
        fig_lb.update_layout(
            barmode="stack", height=max(180, len(labor_df) * 80),
            margin=dict(l=0, r=20, t=10, b=0),
            legend=dict(orientation="h", y=1.18, font=dict(color="#94a3b8", size=13)),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#64748b", size=12)),
            yaxis=dict(tickfont=dict(color="#cbd5e1", size=14), automargin=True),
            bargap=0.3,
        )
        st.plotly_chart(fig_lb, use_container_width=True, config={"staticPlot": True})


load_data()
render()
