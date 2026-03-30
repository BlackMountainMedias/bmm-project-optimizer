"""BMM Project Optimizer — V1 Dashboard (multi-page with native nav)."""
import os
import streamlit as st
from shared import apply_theme, LOGO_PATH

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="BMM Project Optimizer", layout="wide",
                   page_icon="^", initial_sidebar_state="auto")
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
# Sidebar — logo (nav is handled natively above)
# ---------------------------------------------------------------------------
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=180)
    st.sidebar.markdown("")

# ---------------------------------------------------------------------------
# Mobile: make the built-in sidebar toggle always visible + styled
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @media (max-width: 768px) {
        /* Make Streamlit's own sidebar toggle bigger and always visible */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            bottom: 20px !important;
            right: 20px !important;
            top: auto !important;
            left: auto !important;
            z-index: 999999 !important;
        }
        [data-testid="stSidebarCollapsedControl"] button {
            background: #ff6b35 !important;
            color: white !important;
            border: none !important;
            border-radius: 50% !important;
            width: 56px !important;
            height: 56px !important;
            min-height: 56px !important;
            box-shadow: 0 4px 16px rgba(255,107,53,0.4) !important;
        }
        [data-testid="stSidebarCollapsedControl"] button svg {
            fill: white !important;
            stroke: white !important;
            width: 28px !important;
            height: 28px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Run the selected page
# ---------------------------------------------------------------------------
pages.run()
