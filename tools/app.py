"""BMM Project Optimizer — V1 Dashboard (multi-page with native nav)."""
import os
import streamlit as st
from shared import apply_theme, LOGO_PATH

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="BMM Project Optimizer", layout="wide",
                   page_icon="^", initial_sidebar_state="expanded")
apply_theme()


pages = st.navigation([
    st.Page("pages/portfolio.py", title="Portfolio Overview", icon=":material/dashboard:", default=True),
    st.Page("pages/project_detail.py", title="Project Detail", icon=":material/search:"),
    st.Page("pages/change_orders.py", title="Change Orders", icon=":material/swap_horiz:"),
    st.Page("pages/schedule.py", title="Schedule", icon=":material/calendar_month:"),
    st.Page("pages/labor.py", title="Labor", icon=":material/engineering:"),
    st.Page("pages/materials.py", title="Materials", icon=":material/local_shipping:"),
    st.Page("pages/outliers.py", title="Outliers", icon=":material/warning:"),
    st.Page("pages/upload.py", title="Upload Data", icon=":material/upload_file:"),
    st.Page("pages/ai_assistant.py", title="AI Assistant", icon=":material/smart_toy:"),
])

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Run the selected page
# ---------------------------------------------------------------------------
pages.run()
