"""Material Delivery Risk page."""
import streamlit as st
import pandas as pd
from shared import MAT_RISK_COLORS, load_data, demo_callout, is_demo_mode
from calculations import material_risk_summary


def render():
    data = st.session_state["app_data"]
    materials_df = data["materials_df"]

    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h1 style="font-size: 28px; margin-bottom: 4px;">Material Delivery Risk</h1>
        <p style="color: #64748b; font-size: 14px; margin: 0;">
            Track deliveries, flag delays, and quantify idle crew exposure
        </p>
    </div>
    """, unsafe_allow_html=True)

    if is_demo_mode():
        demo_callout("📦", "Backordered materials idle your crews and burn money. Northgate's fire suppression heads are backordered -- that's a crew sitting on site waiting, costing you every day.")

    if materials_df is None or materials_df.empty:
        st.info("No material data available. Upload material orders or use demo data.")
        return

    mat_df, mat_stats = material_risk_summary(materials_df)

    # KPI row
    mt_kcols = st.columns(5)
    mt_kcols[0].metric("Total Orders", f"{mat_stats['total_orders']}")
    mt_kcols[1].metric("Total Value", f"${mat_stats['total_value']:,.0f}")
    mt_kcols[2].metric("Delivered", f"{mat_stats.get('delivered', 0)}")
    mt_kcols[3].metric("At Risk", f"{mat_stats.get('at_risk', 0)}")
    at_risk_val = mat_stats.get('at_risk_value', 0)
    mt_kcols[4].metric("At-Risk Value", f"${at_risk_val:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Material risk cards for at-risk items
    if "Risk" in mat_df.columns:
        at_risk_items = mat_df[mat_df["Risk"].isin(["Overdue", "High Risk", "Watch"])]
        if not at_risk_items.empty:
            st.markdown('<div class="section-header">At-Risk Deliveries</div>', unsafe_allow_html=True)
            for _, item in at_risk_items.iterrows():
                risk = item.get("Risk", "On Track")
                color = MAT_RISK_COLORS.get(risk, "#64748b")
                vendor = item.get("Vendor", "")
                value = item.get("Value", 0)
                delivery = item.get("Delivery", "")
                delivery_str = str(delivery)[:10] if pd.notna(delivery) else "TBD"

                st.markdown(f"""
                <div style="background: #111827; border: 1px solid #1e293b; border-left: 4px solid {color};
                            border-radius: 12px; padding: 14px 18px; margin-bottom: 8px;
                            display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                            <span style="background: {color}; color: white; font-size: 10px; font-weight: 700;
                                         padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">{risk}</span>
                            <span style="color: #f1f5f9; font-size: 14px; font-weight: 600;">{item.get('Material', '')}</span>
                        </div>
                        <div style="color: #64748b; font-size: 12px;">
                            {item.get('Project', '')} / {item.get('Phase', '')} — {vendor}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 16px; font-weight: 700; color: {color};">${value:,.0f}</div>
                        <div style="color: #64748b; font-size: 12px;">Due: {delivery_str}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Full materials table
    st.markdown('<div class="section-header">All Material Orders</div>', unsafe_allow_html=True)
    fmt_mat = {}
    if "Value" in mat_df.columns:
        fmt_mat["Value"] = "${:,.0f}"
    st.dataframe(
        mat_df.style.format(fmt_mat) if fmt_mat else mat_df,
        use_container_width=True, hide_index=True,
    )


load_data()
render()
