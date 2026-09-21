"""Floating AI button + chat panel UI + Home page UI components."""
import streamlit as st
import random
import folium
from folium.plugins import Fullscreen, MarkerCluster


# ------------------------------------------------------------------
# CSS
# ------------------------------------------------------------------
def inject_home_css():
    st.markdown("""
<style>
.moil-header {
    background: linear-gradient(90deg, #0d3b2e 0%, #00695c 55%, #00897b 100%);
    color: #fff; padding: 14px 22px; border-radius: 12px; margin-bottom: 14px;
    display: flex; justify-content: space-between; align-items: center;
    box-shadow: 0 4px 18px rgba(0, 105, 92, 0.28);
}
.moil-header h1 { margin: 0; font-size: 1.35rem; font-weight: 700; letter-spacing: 0.04em; }
.moil-header .sub { margin: 2px 0 0 0; font-size: 0.82rem; opacity: 0.9; }
.moil-status {
    background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px; padding: 6px 14px; font-size: 0.78rem;
    display: flex; align-items: center; gap: 8px;
}
.moil-status .dot {
    width: 8px; height: 8px; background: #69f0ae; border-radius: 50%;
    box-shadow: 0 0 6px #69f0ae;
}
.kpi-card {
    background: #fff; border: 1px solid #e0e7e4; border-radius: 12px;
    padding: 14px 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: box-shadow 0.2s ease, transform 0.2s ease; height: 100%;
}
.kpi-card:hover { box-shadow: 0 6px 20px rgba(0,105,92,0.12); transform: translateY(-2px); }
.kpi-icon { font-size: 1.15rem; margin-bottom: 4px; }
.kpi-value { font-size: 1.55rem; font-weight: 700; color: #00695c; line-height: 1.15; margin: 0; }
.kpi-label {
    font-size: 0.78rem; color: #546e7a; margin: 2px 0 0 0; font-weight: 500;
    text-transform: uppercase; letter-spacing: 0.03em;
}
.kpi-hint { font-size: 0.72rem; color: #78909c; margin-top: 4px; }
.kpi-trend-up { color: #2e7d32; font-size: 0.75rem; font-weight: 600; }
.map-workspace {
    background: #f7faf9; border: 1px solid #dce5e1; border-radius: 14px;
    padding: 10px 12px 8px 12px; box-shadow: 0 3px 14px rgba(0,0,0,0.06);
}
.map-toolbar-label {
    font-size: 0.72rem; font-weight: 600; color: #546e7a;
    text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px;
}
.panel-title {
    font-size: 0.8rem; font-weight: 700; color: #00695c; text-transform: uppercase;
    letter-spacing: 0.04em; margin: 0 0 10px 0; border-bottom: 2px solid #e0f2f1; padding-bottom: 6px;
}
.summary-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 5px 0; font-size: 0.85rem; border-bottom: 1px solid #f0f4f3;
}
.summary-row:last-child { border-bottom: none; }
.badge-high { color: #2e7d32; font-weight: 600; }
.badge-med  { color: #f9a825; font-weight: 600; }
.badge-low  { color: #c62828; font-weight: 600; }
.map-footer {
    font-size: 0.75rem; color: #607d8b; padding: 6px 4px 2px 4px;
    display: flex; justify-content: space-between;
}
</style>
""", unsafe_allow_html=True)


def render_header():
    st.markdown("""
<div class="moil-header">
  <div>
    <h1>⛏️ MOIL MANGANESE INTELLIGENCE</h1>
    <p class="sub">Integrated Mining · Geological · Satellite Command Center</p>
  </div>
  <div class="moil-status"><span class="dot"></span> System Online · GIS View</div>
</div>
""", unsafe_allow_html=True)


def render_kpis():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
<div class="kpi-card">
  <div class="kpi-icon">🏭</div>
  <p class="kpi-value">13</p>
  <p class="kpi-label">Active Mines</p>
  <p class="kpi-hint">Across 5 states</p>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="kpi-card">
  <div class="kpi-icon">📦</div>
  <p class="kpi-value">18.03</p>
  <p class="kpi-label">FY25 Production</p>
  <p class="kpi-hint"><span class="kpi-trend-up">↑ +2.67% YoY</span> · Lakh MT</p>
</div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class="kpi-card">
  <div class="kpi-icon">🎯</div>
  <p class="kpi-value">200+</p>
  <p class="kpi-label">High-Conf. Targets</p>
  <p class="kpi-hint">Drill priority zones</p>
</div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
<div class="kpi-card">
  <div class="kpi-icon">🗺️</div>
  <p class="kpi-value">5</p>
  <p class="kpi-label">States Covered</p>
  <p class="kpi-hint">MP · MH · OD · KA · AP</p>
</div>""", unsafe_allow_html=True)


def render_target_summary(targets):
    high = med = low = 0
    for _, _, col in targets:
        if col == "#2e7d32":
            high += 1
        elif col == "#f9a825":
            med += 1
        else:
            low += 1

    st.markdown('<p class="panel-title">Drill Target Summary</p>', unsafe_allow_html=True)
    st.markdown(f"""
<div class="summary-row"><span>🟢 High Confidence</span><span class="badge-high">{high}</span></div>
<div class="summary-row"><span>🟡 Medium Confidence</span><span class="badge-med">{med}</span></div>
<div class="summary-row"><span>🔴 Low Confidence</span><span class="badge-low">{low}</span></div>
<div class="summary-row"><span><b>Total Visible</b></span><span><b>{high + med + low}</b></span></div>
""", unsafe_allow_html=True)


def render_quick_guide():
    st.markdown('<p class="panel-title">Quick Guide</p>', unsafe_allow_html=True)
    st.caption(
        "• Click a **mine polygon** for details\n\n"
        "• Switch **basemap** above the map\n\n"
        "• Toggle layers via map control (top-right)"
    )


def render_map_toolbar():
    st.markdown('<p class="map-toolbar-label">Basemap</p>', unsafe_allow_html=True)
    views = ["Satellite", "Terrain", "Street Map", "Light Map"]
    cols = st.columns(4)
    for i, v in enumerate(views):
        active = st.session_state.map_view == v
        label = f"● {v}" if active else v
        if cols[i].button(label, key=f"bm_{v}", use_container_width=True):
            st.session_state.map_view = v
            st.rerun()

    t1, t2 = st.columns(2)
    with t1:
        if st.button("⌂ Reset View", key="btn_reset_view", use_container_width=True):
            st.session_state.map_center = [21.75, 80.0]
            st.session_state.map_zoom = 8
            st.rerun()
    with t2:
        if st.button("⊡ Fit All Mines", key="btn_fit_all", use_container_width=True):
            st.session_state.map_center = [20.5, 80.5]
            st.session_state.map_zoom = 6
            st.rerun()


# ------------------------------------------------------------------
# UPDATED POPUP – now includes Coordinates
# ------------------------------------------------------------------
def _popup_html(mine):
    lat, lon = mine["center"]
    return f"""
    <div style="font-family:'Segoe UI',Arial,sans-serif; width:270px; padding:4px 2px;">
      <div style="font-size:14px; font-weight:700; color:#00695c; margin-bottom:6px;
                  border-bottom:2px solid #e0f2f1; padding-bottom:4px;">{mine['name']}</div>
      <div style="font-size:11px; color:#fff; background:#00695c; display:inline-block;
                  padding:2px 8px; border-radius:10px; margin-bottom:8px;">{mine['status'].upper()}</div>
      <table style="width:100%; font-size:12px; color:#37474f; border-collapse:collapse;">
        <tr>
            <td style="padding:3px 0; color:#78909c;">State</td>
            <td style="padding:3px 0; text-align:right; font-weight:600;">{mine['state']}</td>
        </tr>
        <tr>
            <td style="padding:3px 0; color:#78909c;">District</td>
            <td style="padding:3px 0; text-align:right; font-weight:600;">{mine['district']}</td>
        </tr>
        <tr>
            <td style="padding:3px 0; color:#78909c;">Type</td>
            <td style="padding:3px 0; text-align:right; font-weight:600;">{mine['type']}</td>
        </tr>
        <tr>
            <td style="padding:3px 0; color:#78909c;">Importance</td>
            <td style="padding:3px 0; text-align:right; font-weight:700; color:#e65100;">{mine['importance']*100:.0f}%</td>
        </tr>
        <tr>
            <td style="padding:3px 0; color:#78909c;">Area</td>
            <td style="padding:3px 0; text-align:right; font-weight:600;">{mine['area_km2']} km²</td>
        </tr>
        <tr>
            <td style="padding:3px 0; color:#78909c;">Coordinates</td>
            <td style="padding:3px 0; text-align:right; font-weight:600;">{lat:.4f}° N, {lon:.4f}° E</td>
        </tr>
      </table>
    </div>
    """


def ensure_drill_targets(mine_areas):
    if "drill_targets" not in st.session_state:
        random.seed(42)
        targets = []
        for mine in mine_areas:
            lat, lon = mine["center"]
            n = 22 if mine["importance"] > 0.9 else 16
            for _ in range(n):
                plat = lat + random.uniform(-0.005, 0.005)
                plon = lon + random.uniform(-0.005, 0.005)
                conf = random.uniform(0.55, 0.97)
                col = "#2e7d32" if conf > 0.85 else "#f9a825" if conf > 0.70 else "#c62828"
                targets.append((plat, plon, col))
        st.session_state.drill_targets = targets
    return st.session_state.drill_targets


def build_map(mine_areas, all_targets):
    m = folium.Map(
        location=st.session_state.map_center,
        zoom_start=st.session_state.map_zoom,
        tiles=None, max_zoom=19, control_scale=True,
    )

    folium.TileLayer(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Satellite", max_zoom=19,
        show=(st.session_state.map_view == "Satellite"),
    ).add_to(m)
    folium.TileLayer(
        "OpenStreetMap", name="Street Map", max_zoom=19,
        show=(st.session_state.map_view == "Street Map"),
    ).add_to(m)
    folium.TileLayer(
        "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Light Map", max_zoom=16,
        show=(st.session_state.map_view == "Light Map"),
    ).add_to(m)
    folium.TileLayer(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Terrain", max_zoom=16,
        show=(st.session_state.map_view == "Terrain"),
    ).add_to(m)

    # Mines
    fg = folium.FeatureGroup("Mines")
    open_mine = st.session_state.get("open_popup_mine")

    for mine in mine_areas:
        color = (
            "#e65100" if mine["importance"] >= 0.90
            else "#ff6d00" if mine["importance"] >= 0.75
            else "#ffab00"
        )
        folium.Polygon(
            mine["coords"], color=color, weight=2.5, fill=True,
            fill_color=color, fill_opacity=0.42,
            popup=folium.Popup(_popup_html(mine), max_width=280),
            tooltip=folium.Tooltip(
                f"<b>{mine['name']}</b><br>{mine['status']} · {mine['state']}", sticky=True
            ),
        ).add_to(fg)

        if open_mine == mine["name"]:
            folium.Marker(
                location=mine["center"],
                popup=folium.Popup(_popup_html(mine), max_width=280, show=True),
                icon=folium.Icon(color="green", icon="info-sign"),
            ).add_to(m)

    fg.add_to(m)

    # Drill Targets
    fg2 = folium.FeatureGroup("Drill Targets")
    cl = MarkerCluster().add_to(fg2)
    for lat, lon, col in all_targets:
        folium.CircleMarker(
            [lat, lon], radius=5 if col == "#2e7d32" else 4,
            color=col, fill=True, fill_color=col, fill_opacity=0.88, weight=1,
            tooltip="Drill target",
        ).add_to(cl)
    fg2.add_to(m)

    # Legend
    legend_html = """
    <div style="position:fixed;bottom:28px;left:28px;z-index:9999;background:rgba(255,255,255,0.96);
        border:1px solid #cfd8dc;border-radius:10px;padding:11px 14px;font-size:12px;line-height:1.55;
        color:#263238;box-shadow:0 4px 14px rgba(0,0,0,0.14);font-family:'Segoe UI',Arial,sans-serif;min-width:160px;">
        <div style="font-weight:700;color:#00695c;font-size:12.5px;margin-bottom:6px;
                    border-bottom:1px solid #e0f2f1;padding-bottom:4px;">Map Legend</div>
        <div style="font-weight:600;margin-bottom:2px;">Mine Importance</div>
        <span style="color:#e65100;">■</span> Very High (≥90%)<br>
        <span style="color:#ff6d00;">■</span> High (75–89%)<br>
        <span style="color:#ffab00;">■</span> Moderate<br>
        <div style="font-weight:600;margin:8px 0 2px 0;">Drill Confidence</div>
        <span style="color:#2e7d32;">●</span> High &nbsp;
        <span style="color:#f9a825;">●</span> Medium &nbsp;
        <span style="color:#c62828;">●</span> Low
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    folium.LayerControl(collapsed=True).add_to(m)
    Fullscreen().add_to(m)
    return m


def render_map_footer(n_mines, n_targets, n_states):
    view = st.session_state.get("map_view", "Satellite")
    st.markdown(f"""
<div class="map-footer">
  <span>{n_mines} mines · {n_targets} targets · {n_states} states</span>
  <span>GIS VIEW · {view}</span>
</div>
""", unsafe_allow_html=True)