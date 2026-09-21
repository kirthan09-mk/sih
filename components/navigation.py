"""Top navigation bar for page switching."""
import streamlit as st

PAGES = [
    "Home",
    "Geological Insights",
    "Production & Analytics",
    "Geosatellite Analytics",
    "Production Prediction",
]


def render_top_nav():
    c1, c2 = st.columns([0.07, 0.93])
    with c1:
        if st.button("☰"):
            st.session_state.show_nav = not st.session_state.show_nav
            st.rerun()
    with c2:
        st.markdown(f"### {st.session_state.page}")

    if st.session_state.show_nav:
        st.markdown("---")
        cols = st.columns(len(PAGES))
        for i, p in enumerate(PAGES):
            if cols[i].button(p, use_container_width=True):
                st.session_state.page = p
                st.session_state.show_nav = False
                st.rerun()
        st.markdown("---")