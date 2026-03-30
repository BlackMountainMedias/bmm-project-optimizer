"""Change Order Analysis page."""
import streamlit as st
import plotly.graph_objects as go
from shared import load_data
from calculations import change_order_summary, portfolio_summary


def render():
    data = st.session_state["app_data"]
    df = data["df"]
    co_df = data["co_df"]

    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h1 style="font-size: 28px; margin-bottom: 4px;">Change Order Analysis</h1>
        <p style="color: #64748b; font-size: 14px; margin: 0;">
            Approved scope changes vs true overruns — see where the budget really stands
        </p>
    </div>
    """, unsafe_allow_html=True)

    if co_df is None or co_df.empty:
        st.info("No change order data available. Upload change orders or use demo data.")
        return

    co_summary_df, co_totals = change_order_summary(co_df)
    psummary = portfolio_summary(df)

    # KPI rows — two rows of 3 for readability
    raw_var = df["variance"].sum()
    adj_var = raw_var - co_totals["approved_impact"]

    row1 = st.columns(3)
    row1[0].metric("Total Change Orders", f"{co_totals['total_cos']}")
    row1[1].metric("Approved Impact", f"${co_totals['approved_impact']:,.0f}")
    row1[2].metric("Pending Impact", f"${co_totals['pending_impact']:,.0f}")

    row2 = st.columns(3)
    row2[0].metric("Total CO Impact", f"${co_totals['total_impact']:,.0f}")
    row2[1].metric("True Overrun", f"${adj_var:+,.0f}")
    row2[2].metric("Approved Scope", f"${co_totals['approved_impact']:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Variance breakdown chart — full width, stacked: true overrun + approved CO
    st.markdown('<div class="section-header">Variance Breakdown by Project</div>', unsafe_allow_html=True)
    if "Adjusted Variance" in psummary.columns:
        # CO approved portion = Raw Variance - Adjusted Variance
        co_approved = psummary["Variance"] - psummary["Adjusted Variance"]
        adj_var_vals = psummary["Adjusted Variance"]

        fig_co = go.Figure()
        # True overrun (after removing approved COs)
        fig_co.add_trace(go.Bar(
            y=psummary["Project"], x=adj_var_vals, name="True Overrun",
            orientation="h", marker_color="#ef4444", marker_line_width=0,
            text=[f"${v:,.0f}" for v in adj_var_vals],
            textposition="auto", textfont=dict(color="#f1f5f9", size=12),
        ))
        # Approved CO scope (stacked on top)
        fig_co.add_trace(go.Bar(
            y=psummary["Project"], x=co_approved, name="Approved CO Scope",
            orientation="h", marker_color="#3b82f6", marker_line_width=0,
            text=[f"${v:,.0f}" for v in co_approved],
            textposition="auto", textfont=dict(color="#f1f5f9", size=12),
        ))
        fig_co.update_layout(
            barmode="stack", height=max(180, len(psummary) * 80),
            margin=dict(l=0, r=20, t=10, b=0),
            legend=dict(orientation="h", y=1.18, font=dict(color="#94a3b8", size=13)),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#64748b", size=12),
                       tickformat="$,.0f"),
            yaxis=dict(tickfont=dict(color="#cbd5e1", size=14), automargin=True),
            bargap=0.3,
        )
        st.plotly_chart(fig_co, use_container_width=True, config={"staticPlot": True})

    st.markdown("<br>", unsafe_allow_html=True)

    # Change Orders by Project table
    st.markdown('<div class="section-header">Change Orders by Project</div>', unsafe_allow_html=True)
    if not co_summary_df.empty:
        st.dataframe(
            co_summary_df.style.format({
                "Approved $": "${:,.0f}",
                "Pending $": "${:,.0f}",
                "Total Impact": "${:,.0f}",
            }),
            use_container_width=True, hide_index=True,
        )

    # Detailed CO table
    st.markdown('<div class="section-header">All Change Orders</div>', unsafe_allow_html=True)
    co_display = co_df.copy()
    co_display_cols = ["project_name", "co_number", "description", "cost_impact", "phase", "status"]
    available_co_cols = [c for c in co_display_cols if c in co_display.columns]
    co_display = co_display[available_co_cols]
    rename_co = {"project_name": "Project", "co_number": "CO #", "description": "Description",
                 "cost_impact": "Cost Impact", "phase": "Phase", "status": "Status"}
    co_display = co_display.rename(columns={k: v for k, v in rename_co.items() if k in co_display.columns})
    st.dataframe(
        co_display.style.format({"Cost Impact": "${:,.0f}"}) if "Cost Impact" in co_display.columns else co_display,
        use_container_width=True, hide_index=True,
    )


load_data()
render()
