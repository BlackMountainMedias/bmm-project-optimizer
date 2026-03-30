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
# Mobile: inject a persistent sidebar toggle via JS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    #mobile-nav-btn {
        display: none;
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 999999;
        background: #ff6b35;
        color: white;
        border: none;
        border-radius: 50%;
        width: 56px;
        height: 56px;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 16px rgba(255,107,53,0.4);
    }
    @media (max-width: 768px) {
        #mobile-nav-btn { display: block; }
    }
</style>
<button id="mobile-nav-btn" onclick="
    const btn = window.parent.document.querySelector('[data-testid=\\'stSidebarCollapsedControl\\'] button');
    if (btn) btn.click();
    const btn2 = window.parent.document.querySelector('button[kind=\\'headerNoPadding\\']');
    if (btn2) btn2.click();
">☰</button>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Run the selected page
# ---------------------------------------------------------------------------
pages.run()
