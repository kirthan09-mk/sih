"""
Home page – links to components/home_ui.py for all design.
"""
import streamlit as st
from streamlit_folium import st_folium

from data import get_mine_areas_with_area
from components.home_ui import (
    inject_home_css,
    render_header,
    render_kpis,
    render_target_summary,
    render_quick_guide,
    ensure_drill_targets,
    build_map,
    render_map_footer,
)


def render():
    # Data
    mine_areas = st.session_state.get("mine_areas") or get_mine_areas_with_area()
    if "mine_areas" not in st.session_state:
        st.session_state.mine_areas = mine_areas

    all_targets = ensure_drill_targets(mine_areas)

    # Design
    inject_home_css()
    render_header()
    render_kpis()
    st.markdown("")

    # Wider map + sidebar on the right
    center, right = st.columns([3.6, 1.1])

    with right:
        render_target_summary(all_targets)
        st.markdown("---")
        render_quick_guide()

    with center:
        st.markdown('<div class="map-workspace">', unsafe_allow_html=True)

        # Build map (popup auto-open is handled inside build_map)
        m = build_map(mine_areas, all_targets)

        st_folium(m, width=None, height=600, key="mainmap")

        n_states = len({x["state"] for x in mine_areas})
        render_map_footer(len(mine_areas), len(all_targets), n_states)

        st.markdown("</div>", unsafe_allow_html=True)