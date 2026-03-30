"""Outlier Alerts page."""
import streamlit as st
import pandas as pd
from shared import SEVERITY_COLORS, get_rag_func, load_data
from calculations import run_outlier_detection


def render():
    data = st.session_state["app_data"]
    df = data["df"]
    _rag = get_rag_func()
    df["status"] = df["variance_pct"].apply(_rag)

    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h1 style="font-size: 28px; margin-bottom: 4px;">Outlier Alerts</h1>
        <p style="color: #64748b; font-size: 14px; margin: 0;">
            Statistically anomalous line items flagged by IQR, Z-score, and peer comparison
        </p>
    </div>
    """, unsafe_allow_html=True)

    flags_df, outlier_stats, outlier_by_proj, outlier_by_cat = run_outlier_detection(df)

    if outlier_stats["total_flags"] == 0:
        st.markdown("""
        <div style="background: #111827; border: 1px solid #1e293b; border-radius: 12px;
                    padding: 32px; text-align: center;">
            <div style="font-size: 18px; color: #22c55e; font-weight: 600; margin-bottom: 8px;">
                No Outliers Detected
            </div>
            <div style="color: #64748b; font-size: 14px;">
                All line items are within expected ranges
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # KPI row
    ocols = st.columns(5)
    ocols[0].metric("Outliers Found", f"{outlier_stats['total_flags']}")
    ocols[1].metric("Dollar Impact", f"${outlier_stats['total_dollar_impact']:,.0f}")
    ocols[2].metric("Critical", f"{outlier_stats['critical']}")
    ocols[3].metric("High", f"{outlier_stats['high']}")
    ocols[4].metric("Medium + Low", f"{outlier_stats['medium'] + outlier_stats['low']}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Outlier alert cards - top 10
    st.markdown('<div class="section-header">Top Outlier Alerts</div>', unsafe_allow_html=True)
    top_flags = flags_df.head(10)
    for _, flag in top_flags.iterrows():
        sev = flag["severity"]
        sev_color = SEVERITY_COLORS.get(sev, "#64748b")
        peer_note = ""
        if pd.notna(flag.get("peer_avg_variance_pct")) and flag["peer_avg_variance_pct"] is not None:
            peer_note = f" | Peer avg: {flag['peer_avg_variance_pct']:+.1%}"

        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #1e293b; border-left: 4px solid {sev_color};
                    border-radius: 12px; padding: 16px 20px; margin-bottom: 10px;
                    display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                    <span style="background: {sev_color}; color: white; font-size: 10px; font-weight: 700;
                                 padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">{sev}</span>
                    <span style="color: #f1f5f9; font-size: 14px; font-weight: 600;">{flag['line_item']}</span>
                </div>
                <div style="color: #64748b; font-size: 12px;">
                    {flag['project_name']} / {flag['phase']} / {flag['cost_category']}
                </div>
                <div style="color: #94a3b8; font-size: 11px; margin-top: 4px;">
                    Method: {flag['detection_method']}{peer_note}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 18px; font-weight: 700; color: {sev_color};">
                    ${flag['variance']:+,.0f}
                </div>
                <div style="color: #64748b; font-size: 12px;">
                    {flag['variance_pct']:+.1%} over budget
                </div>
                <div style="color: #94a3b8; font-size: 11px;">
                    Budget: ${flag['budgeted_amount']:,.0f}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Two-column: by project + by category
    st.markdown("<br>", unsafe_allow_html=True)
    ol_left, ol_right = st.columns(2, gap="large")

    with ol_left:
        st.markdown('<div class="section-header">Outliers by Project</div>', unsafe_allow_html=True)
        if not outlier_by_proj.empty:
            for _, r in outlier_by_proj.iterrows():
                sev_color = SEVERITY_COLORS.get(r["worst_severity"], "#64748b")
                st.markdown(f"""
                <div class="risk-row">
                    <div>
                        <div class="risk-label">{r['project_name']}</div>
                        <div class="risk-project">{r['flags']} outlier{'s' if r['flags'] != 1 else ''}</div>
                    </div>
                    <div style="text-align: right;">
                        <div class="risk-amount" style="color: {sev_color};">${r['dollar_impact']:+,.0f}</div>
                        <div style="color: #64748b; font-size: 11px; text-transform: uppercase;">{r['worst_severity']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with ol_right:
        st.markdown('<div class="section-header">Outliers by Category</div>', unsafe_allow_html=True)
        if not outlier_by_cat.empty:
            for _, r in outlier_by_cat.iterrows():
                st.markdown(f"""
                <div class="risk-row">
                    <div>
                        <div class="risk-label">{r['cost_category']}</div>
                        <div class="risk-project">{r['flags']} outlier{'s' if r['flags'] != 1 else ''}</div>
                    </div>
                    <div style="text-align: right;">
                        <div class="risk-amount" style="color: #f59e0b;">${r['dollar_impact']:+,.0f}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


load_data()
render()
