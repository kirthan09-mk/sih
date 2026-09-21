"""
Home page – Operational mines + Predicted Future Mines (14 targets)
"""

import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import Fullscreen

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

# ------------------------------------------------------------------
# 14 Predicted Future Mines
# ------------------------------------------------------------------
PREDICTED_MINES = [
    {
        "name": "Predicted Target – North Balaghat Extension",
        "coords": [[21.855, 80.160],[21.870, 80.175],[21.865, 80.200],[21.845, 80.210],[21.830, 80.190],[21.835, 80.165]],
        "center": [21.850, 80.183],
        "basis": "Sub-surface dominant",
        "indicators": ["High IP chargeability", "Low resistivity", "Magnetic anomaly", "Gravity high"],
        "area_km2": 4.85, "est_tonnage_mt": 2.45, "depth_m": "280 – 420 m",
        "confidence": 87, "state": "Madhya Pradesh", "district": "Balaghat"
    },
    {
        "name": "Predicted Target – Dongri North Extension",
        "coords": [[21.375, 79.835],[21.390, 79.850],[21.385, 79.875],[21.365, 79.885],[21.350, 79.865],[21.355, 79.840]],
        "center": [21.370, 79.858],
        "basis": "Surface dominant",
        "indicators": ["Black manganese outcrops", "Laterite cover", "Prominent exposures"],
        "area_km2": 2.75, "est_tonnage_mt": 1.10, "depth_m": "Shallow – 180 m",
        "confidence": 82, "state": "Maharashtra", "district": "Bhandara"
    },
    {
        "name": "Predicted Target – Kandri South Block",
        "coords": [[21.425, 79.055],[21.440, 79.070],[21.435, 79.095],[21.415, 79.105],[21.400, 79.085],[21.405, 79.060]],
        "center": [21.420, 79.078],
        "basis": "Sub-surface dominant",
        "indicators": ["High IP", "Magnetic anomaly", "Gravity high"],
        "area_km2": 3.10, "est_tonnage_mt": 1.25, "depth_m": "250 – 380 m",
        "confidence": 81, "state": "Maharashtra", "district": "Nagpur"
    },
    {
        "name": "Predicted Target – Ukwa West Block",
        "coords": [[21.955, 80.420],[21.970, 80.435],[21.965, 80.460],[21.945, 80.470],[21.930, 80.450],[21.935, 80.425]],
        "center": [21.950, 80.443],
        "basis": "Both Surface + Sub-surface",
        "indicators": ["Laterite cover", "Old workings", "High IP", "Magnetic anomaly"],
        "area_km2": 3.20, "est_tonnage_mt": 1.35, "depth_m": "220 – 350 m",
        "confidence": 79, "state": "Madhya Pradesh", "district": "Balaghat"
    },
    {
        "name": "Predicted Target – Chikla East Prospect",
        "coords": [[21.420, 79.715],[21.435, 79.730],[21.430, 79.755],[21.410, 79.765],[21.395, 79.745],[21.400, 79.720]],
        "center": [21.415, 79.738],
        "basis": "Both Surface + Sub-surface",
        "indicators": ["Shear zones", "High IP chargeability", "Low resistivity"],
        "area_km2": 2.40, "est_tonnage_mt": 0.95, "depth_m": "200 – 320 m",
        "confidence": 74, "state": "Maharashtra", "district": "Bhandara"
    },
    {
        "name": "Predicted Target – Tirodi Extension",
        "coords": [[21.735, 79.695],[21.750, 79.710],[21.745, 79.735],[21.725, 79.745],[21.710, 79.725],[21.715, 79.700]],
        "center": [21.730, 79.718],
        "basis": "Surface dominant",
        "indicators": ["Laterite cover", "Old workings", "Shear zones"],
        "area_km2": 2.15, "est_tonnage_mt": 0.78, "depth_m": "Shallow – 200 m",
        "confidence": 71, "state": "Madhya Pradesh", "district": "Balaghat"
    },
    {
        "name": "Predicted Target – Munsar East Block",
        "coords": [[21.460, 79.090],[21.475, 79.105],[21.470, 79.130],[21.450, 79.140],[21.435, 79.120],[21.440, 79.095]],
        "center": [21.455, 79.113],
        "basis": "Sub-surface dominant",
        "indicators": ["Magnetic anomaly", "High IP", "Low resistivity"],
        "area_km2": 2.60, "est_tonnage_mt": 0.88, "depth_m": "230 – 340 m",
        "confidence": 73, "state": "Maharashtra", "district": "Nagpur"
    },
    {
        "name": "Predicted Target – Gumgaon North",
        "coords": [[21.400, 79.150],[21.415, 79.165],[21.410, 79.190],[21.390, 79.200],[21.375, 79.180],[21.380, 79.155]],
        "center": [21.395, 79.173],
        "basis": "Both Surface + Sub-surface",
        "indicators": ["Laterite cover", "Shear zones", "Magnetic anomaly"],
        "area_km2": 2.30, "est_tonnage_mt": 0.72, "depth_m": "180 – 290 m",
        "confidence": 70, "state": "Maharashtra", "district": "Nagpur"
    },
    {
        "name": "Predicted Target – Sitapatore South",
        "coords": [[21.640, 79.640],[21.655, 79.655],[21.650, 79.680],[21.630, 79.690],[21.615, 79.670],[21.620, 79.645]],
        "center": [21.635, 79.663],
        "basis": "Surface dominant",
        "indicators": ["Laterite cover", "Old workings"],
        "area_km2": 1.85, "est_tonnage_mt": 0.45, "depth_m": "Shallow – 160 m",
        "confidence": 62, "state": "Madhya Pradesh", "district": "Balaghat"
    },
    {
        "name": "Predicted Target – Beldongri West",
        "coords": [[21.310, 79.200],[21.325, 79.215],[21.320, 79.240],[21.300, 79.250],[21.285, 79.230],[21.290, 79.205]],
        "center": [21.305, 79.223],
        "basis": "Sub-surface dominant",
        "indicators": ["Weak magnetic anomaly", "Moderate IP response"],
        "area_km2": 1.95, "est_tonnage_mt": 0.52, "depth_m": "200 – 300 m",
        "confidence": 58, "state": "Maharashtra", "district": "Nagpur"
    },
    {
        "name": "Predicted Target – Chhindwara Prospect",
        "coords": [[22.070, 78.950],[22.085, 78.965],[22.080, 78.990],[22.060, 79.000],[22.045, 78.980],[22.050, 78.955]],
        "center": [22.065, 78.973],
        "basis": "Both Surface + Sub-surface",
        "indicators": ["Laterite cover", "Shear zones", "Limited geophysics"],
        "area_km2": 2.50, "est_tonnage_mt": 0.65, "depth_m": "Moderate – 250 m",
        "confidence": 55, "state": "Madhya Pradesh", "district": "Chhindwara"
    },
    {
        "name": "Predicted Target – Sandur North Block",
        "coords": [[15.130, 76.540],[15.145, 76.555],[15.140, 76.580],[15.120, 76.590],[15.105, 76.570],[15.110, 76.545]],
        "center": [15.125, 76.563],
        "basis": "Surface dominant",
        "indicators": ["Black manganese outcrops", "Laterite cover"],
        "area_km2": 2.80, "est_tonnage_mt": 0.70, "depth_m": "Shallow – 150 m",
        "confidence": 61, "state": "Karnataka", "district": "Ballari"
    },
    {
        "name": "Predicted Target – Bonai West Extension",
        "coords": [[21.840, 85.200],[21.855, 85.215],[21.850, 85.240],[21.830, 85.250],[21.815, 85.230],[21.820, 85.205]],
        "center": [21.835, 85.223],
        "basis": "Both Surface + Sub-surface",
        "indicators": ["Laterite cover", "Magnetic anomaly", "Gravity high"],
        "area_km2": 2.90, "est_tonnage_mt": 0.85, "depth_m": "Moderate – 280 m",
        "confidence": 64, "state": "Odisha", "district": "Sundargarh"
    },
    {
        "name": "Predicted Target – Joda South Prospect",
        "coords": [[21.980, 85.420],[21.995, 85.435],[21.990, 85.460],[21.970, 85.470],[21.955, 85.450],[21.960, 85.425]],
        "center": [21.975, 85.443],
        "basis": "Surface dominant",
        "indicators": ["Black manganese outcrops", "Laterite cover", "Old workings"],
        "area_km2": 2.20, "est_tonnage_mt": 0.58, "depth_m": "Shallow – 170 m",
        "confidence": 59, "state": "Odisha", "district": "Keonjhar"
    },
]


def build_predicted_mines_map(predicted_mines):
    m = folium.Map(location=[21.50, 80.50], zoom_start=7, tiles=None, control_scale=True)

    folium.TileLayer(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Satellite", max_zoom=19, show=True
    ).add_to(m)
    folium.TileLayer("OpenStreetMap", name="Street Map", show=False).add_to(m)

    for mine in predicted_mines:
        if mine["confidence"] >= 82:
            color = "#2e7d32"
        elif mine["confidence"] >= 70:
            color = "#f9a825"
        else:
            color = "#c62828"

        lat, lon = mine["center"]

        popup_html = f"""
        <div style="font-family:'Segoe UI',Arial,sans-serif; width:280px; padding:6px;">
            <div style="font-size:15px; font-weight:700; color:#00695c; margin-bottom:8px;
                        border-bottom:2px solid #e0f2f1; padding-bottom:5px;">{mine['name']}</div>
            <div style="margin-bottom:8px;">
                <span style="background:#00695c; color:white; padding:3px 10px; border-radius:12px; font-size:11px;">{mine['basis']}</span>
            </div>
            <table style="width:100%; font-size:12.5px; color:#37474f; border-collapse:collapse;">
                <tr><td style="padding:4px 0; color:#78909c;">Predicted Area</td>
                    <td style="padding:4px 0; text-align:right; font-weight:600;">{mine['area_km2']} km²</td></tr>
                <tr><td style="padding:4px 0; color:#78909c;">Est. Mn Tonnage</td>
                    <td style="padding:4px 0; text-align:right; font-weight:700; color:#e65100;">{mine['est_tonnage_mt']} MT</td></tr>
                <tr><td style="padding:4px 0; color:#78909c;">Predicted Depth</td>
                    <td style="padding:4px 0; text-align:right; font-weight:600;">{mine['depth_m']}</td></tr>
                <tr><td style="padding:4px 0; color:#78909c;">Drill Confidence</td>
                    <td style="padding:4px 0; text-align:right; font-weight:700; color:{color};">{mine['confidence']}%</td></tr>
                <tr><td style="padding:4px 0; color:#78909c;">Location</td>
                    <td style="padding:4px 0; text-align:right; font-weight:600;">{mine['district']}, {mine['state']}</td></tr>
                <tr><td style="padding:4px 0; color:#78909c;">Coordinates</td>
                    <td style="padding:4px 0; text-align:right; font-weight:600;">{lat:.4f}° N, {lon:.4f}° E</td></tr>
            </table>
            <div style="margin-top:10px; font-size:12px;">
                <b style="color:#00695c;">Key Indicators:</b><br>{" • ".join(mine['indicators'])}
            </div>
        </div>
        """

        folium.Polygon(
            locations=mine["coords"], color=color, weight=2.5, fill=True,
            fill_color=color, fill_opacity=0.45,
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=folium.Tooltip(f"<b>{mine['name']}</b><br>Confidence: {mine['confidence']}%", sticky=True)
        ).add_to(m)

        folium.CircleMarker(
            location=mine["center"], radius=6, color=color, fill=True,
            fill_color=color, fill_opacity=0.9, tooltip=mine["name"]
        ).add_to(m)

    legend_html = """
    <div style="position:fixed; bottom:30px; left:30px; z-index:9999;
                background:rgba(255,255,255,0.96); border:1px solid #cfd8dc;
                border-radius:10px; padding:12px 16px; font-size:12.5px;
                box-shadow:0 4px 14px rgba(0,0,0,0.15); font-family:Segoe UI,Arial;">
        <div style="font-weight:700; color:#00695c; margin-bottom:6px;">Predicted Targets</div>
        <span style="color:#2e7d32;">■</span> High Confidence (≥82%)<br>
        <span style="color:#f9a825;">■</span> Medium Confidence (70–81%)<br>
        <span style="color:#c62828;">■</span> Lower Confidence (<70%)
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    folium.LayerControl(collapsed=True).add_to(m)
    Fullscreen().add_to(m)
    return m


def render():
    mine_areas = st.session_state.get("mine_areas") or get_mine_areas_with_area()
    if "mine_areas" not in st.session_state:
        st.session_state.mine_areas = mine_areas

    all_targets = ensure_drill_targets(mine_areas)

    inject_home_css()
    render_header()
    render_kpis()
    st.markdown("")

    center, right = st.columns([3.6, 1.1])

    with right:
        render_target_summary(all_targets)
        st.markdown("---")
        render_quick_guide()

    with center:
        st.markdown('<div class="map-workspace">', unsafe_allow_html=True)
        m = build_map(mine_areas, all_targets)
        st_folium(m, width=None, height=600, key="mainmap")
        n_states = len({x["state"] for x in mine_areas})
        render_map_footer(len(mine_areas), len(all_targets), n_states)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔮 Predicted Future Mine Targets")
    st.caption("AI + Geophysical exploration targets. Click any polygon for full details including coordinates.")

    pred_map = build_predicted_mines_map(PREDICTED_MINES)
    st_folium(pred_map, width=None, height=520, key="predicted_mines_map")