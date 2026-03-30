"""Schedule Intelligence page."""
import streamlit as st
from shared import SCHED_COLORS, load_data
from calculations import schedule_alerts


def render():
    data = st.session_state["app_data"]
    schedule_df = data["schedule_df"]

    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h1 style="font-size: 28px; margin-bottom: 4px;">Schedule Intelligence</h1>
        <p style="color: #64748b; font-size: 14px; margin: 0;">
            Task slippage detection — flag delays before they become cost overruns
        </p>
    </div>
    """, unsafe_allow_html=True)

    if schedule_df is None or schedule_df.empty:
        st.info("No schedule data available. Upload a project schedule or use demo data.")
        return

    sched_alerts_df, sched_stats = schedule_alerts(schedule_df)

    # KPI row
    sc_kcols = st.columns(5)
    sc_kcols[0].metric("Total Tasks", f"{sched_stats['total_tasks']}")
    sc_kcols[1].metric("Slipping", f"{sched_stats['slipping']}")
    sc_kcols[2].metric("At Risk", f"{sched_stats['at_risk']}")
    sc_kcols[3].metric("On Track", f"{sched_stats['on_track']}")
    sc_kcols[4].metric("Complete", f"{sched_stats['complete']}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Schedule alert cards
    st.markdown('<div class="section-header">Task Status</div>', unsafe_allow_html=True)
    for _, task in sched_alerts_df.iterrows():
        color = SCHED_COLORS.get(task["Risk Level"], "#64748b")
        slip_text = f"{task['Slip Days']}d slip" if task['Slip Days'] > 0 else ""
        pct = task.get("% Complete", 0) or 0

        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #1e293b; border-left: 4px solid {color};
                    border-radius: 12px; padding: 14px 18px; margin-bottom: 8px;
                    display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="color: #f1f5f9; font-size: 14px; font-weight: 600;">{task['Task']}</div>
                <div style="color: #64748b; font-size: 12px;">{task['Project']} / {task['Phase']}</div>
                <div style="color: {color}; font-size: 12px; margin-top: 4px;">{task['Status']}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 18px; font-weight: 700; color: {color};">{pct:.0f}%</div>
                <div style="color: #64748b; font-size: 12px;">{slip_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


load_data()
render()
