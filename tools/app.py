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
# Mobile: inject JS to open sidebar on button click
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    #bmm-menu-btn {
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
        -webkit-tap-highlight-color: transparent;
        touch-action: manipulation;
    }
    @media (max-width: 768px) {
        #bmm-menu-btn { display: block; }
    }
</style>
<script>
function bmmOpenSidebar() {
    // Try all known Streamlit sidebar toggle selectors
    var selectors = [
        '[data-testid="stSidebarCollapsedControl"] button',
        '[data-testid="collapsedControl"] button',
        'button[kind="headerNoPadding"]',
        '[data-testid="stHeader"] button'
    ];
    for (var i = 0; i < selectors.length; i++) {
        var el = parent.document.querySelector(selectors[i]);
        if (el) { el.click(); return; }
    }
}
</script>
<div id="bmm-menu-btn" ontouchstart="bmmOpenSidebar()" onclick="bmmOpenSidebar()">&#9776;</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Run the selected page
# ---------------------------------------------------------------------------
pages.run()
