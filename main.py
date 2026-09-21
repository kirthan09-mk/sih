"""
MOIL Manganese Platform – main entry point.
Run: streamlit run main.py
"""
import streamlit as st

from styles import inject_global_css
from components.navigation import render_top_nav
from components.chat import render_ai_button_and_panel
from data import get_mine_areas_with_area

from pages.home import render as render_home
from pages.geological import render as render_geological
from pages.production import render as render_production
from pages.satellite import render as render_satellite
from pages.prediction import render as render_prediction   # ← ADD THIS


def init_session_state():
    defaults = {
        "page": "Home",
        "show_chat": False,
        "chat_history": [],
        "map_center": [21.75, 80.0],
        "map_zoom": 8,
        "map_view": "Satellite",
        "show_nav": False,
        "areas_computed": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if not st.session_state.areas_computed:
        st.session_state.mine_areas = get_mine_areas_with_area()
        st.session_state.areas_computed = True


def main():
    st.set_page_config(
        page_title="MOIL Manganese Platform",
        page_icon="⛏️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_global_css()
    init_session_state()
    render_top_nav()
    render_ai_button_and_panel()

    page = st.session_state.page
    if page == "Home":
        render_home()
    elif page == "Geological Insights":
        render_geological()
    elif page == "Production & Analytics":
        render_production()
    elif page == "Satellite Intelligence":
        render_satellite()
    elif page == "Production Prediction":          # ← ADD THIS
        render_prediction()


if __name__ == "__main__":
    main()