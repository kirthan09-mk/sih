

"""Satellite Intelligence page."""
import streamlit as st
import folium
from streamlit_folium import st_folium

MINE_DATA = {
    "balaghat": {
        "name": "Balaghat",
        "lat": 21.8167,
        "lon": 80.1833,
        "moisture": "19%",
        "ndvi": "0.48",
        "rainfall": "52 mm",
        "temp": "31.8°C",
        "polygon": [
            [21.8240, 80.1720], [21.8265, 80.1815], [21.8230, 80.1935],
            [21.8155, 80.1970], [21.8080, 80.1910], [21.8065, 80.1785], [21.8120, 80.1695],
        ],
        "drill_points": [
            {"name": "Drill-BH-01", "lat": 21.8185, "lon": 80.1852, "depth": "125m", "status": "Completed"},
            {"name": "Drill-BH-02", "lat": 21.8148, "lon": 80.1815, "depth": "98m", "status": "Completed"},
            {"name": "Drill-BH-03", "lat": 21.8202, "lon": 80.1878, "depth": "152m", "status": "In Progress"},
            {"name": "Drill-BH-04", "lat": 21.8155, "lon": 80.1790, "depth": "110m", "status": "Completed"},
        ]
    },
    "ukwa": {
        "name": "Ukwa",
        "lat": 21.9750,
        "lon": 80.4667,
        "moisture": "18%",
        "ndvi": "0.45",
        "rainfall": "48 mm",
        "temp": "32.1°C",
        "polygon": [
            [21.9825, 80.4550], [21.9850, 80.4640], [21.9810, 80.4765],
            [21.9735, 80.4800], [21.9670, 80.4730], [21.9660, 80.4605], [21.9720, 80.4520],
        ],
        "drill_points": [
            {"name": "Drill-UK-01", "lat": 21.9768, "lon": 80.4685, "depth": "85m", "status": "Completed"},
            {"name": "Drill-UK-02", "lat": 21.9732, "lon": 80.4648, "depth": "112m", "status": "Completed"},
            {"name": "Drill-UK-03", "lat": 21.9775, "lon": 80.4701, "depth": "95m", "status": "Planned"},
        ]
    },
    "dongri": {
        "name": "Dongri Buzurg",
        "lat": 21.5500,
        "lon": 79.8500,
        "moisture": "17%",
        "ndvi": "0.41",
        "rainfall": "45 mm",
        "temp": "33.0°C",
        "polygon": [
            [21.5570, 79.8390], [21.5595, 79.8485], [21.5555, 79.8610],
            [21.5480, 79.8640], [21.5425, 79.8560], [21.5435, 79.8430], [21.5500, 79.8365],
        ],
        "drill_points": [
            {"name": "Drill-DB-01", "lat": 21.5518, "lon": 79.8522, "depth": "72m", "status": "Completed"},
            {"name": "Drill-DB-02", "lat": 21.5485, "lon": 79.8478, "depth": "88m", "status": "Completed"},
        ]
    },
    "chikla": {
        "name": "Chikla",
        "lat": 21.5500,
        "lon": 79.9500,
        "moisture": "16%",
        "ndvi": "0.39",
        "rainfall": "43 mm",
        "temp": "32.7°C",
        "polygon": [
            [21.5575, 79.9390], [21.5600, 79.9490], [21.5555, 79.9615],
            [21.5480, 79.9640], [21.5420, 79.9555], [21.5440, 79.9420], [21.5505, 79.9365],
        ],
        "drill_points": [
            {"name": "Drill-CH-01", "lat": 21.5515, "lon": 79.9520, "depth": "78m", "status": "Completed"},
            {"name": "Drill-CH-02", "lat": 21.5482, "lon": 79.9475, "depth": "105m", "status": "In Progress"},
            {"name": "Drill-CH-03", "lat": 21.5530, "lon": 79.9535, "depth": "91m", "status": "Completed"},
        ]
    },
    "nagpur": {
        "name": "Nagpur Region",
        "lat": 21.1458,
        "lon": 79.0882,
        "moisture": "15%",
        "ndvi": "0.37",
        "rainfall": "40 mm",
        "temp": "33.5°C",
        "polygon": [
            [21.1530, 79.0770], [21.1560, 79.0870], [21.1515, 79.0995],
            [21.1430, 79.1020], [21.1375, 79.0930], [21.1390, 79.0800], [21.1455, 79.0745],
        ],
        "drill_points": [
            {"name": "Drill-NG-01", "lat": 21.1480, "lon": 79.0905, "depth": "65m", "status": "Completed"},
        ]
    },
    "sandur": {
        "name": "Sandur",
        "lat": 15.0860,
        "lon": 76.5460,
        "moisture": "14%",
        "ndvi": "0.34",
        "rainfall": "38 mm",
        "temp": "34.2°C",
        "polygon": [
            [15.0935, 76.5350], [15.0960, 76.5450], [15.0915, 76.5575],
            [15.0830, 76.5600], [15.0775, 76.5510], [15.0790, 76.5380], [15.0855, 76.5325],
        ],
        "drill_points": [
            {"name": "Drill-SD-01", "lat": 15.0885, "lon": 76.5485, "depth": "55m", "status": "Completed"},
            {"name": "Drill-SD-02", "lat": 15.0835, "lon": 76.5430, "depth": "70m", "status": "Planned"},
        ]
    },
    "bonai": {
        "name": "Bonai",
        "lat": 21.8167,
        "lon": 85.2333,
        "moisture": "20%",
        "ndvi": "0.51",
        "rainfall": "55 mm",
        "temp": "30.9°C",
        "polygon": [
            [21.8240, 85.2220], [21.8265, 85.2315], [21.8230, 85.2435],
            [21.8155, 85.2470], [21.8080, 85.2410], [21.8065, 85.2285], [21.8120, 85.2195],
        ],
        "drill_points": [
            {"name": "Drill-BN-01", "lat": 21.8185, "lon": 85.2355, "depth": "102m", "status": "Completed"},
        ]
    },
    "joda": {
        "name": "Joda",
        "lat": 22.0167,
        "lon": 85.4333,
        "moisture": "19%",
        "ndvi": "0.49",
        "rainfall": "53 mm",
        "temp": "31.2°C",
        "polygon": [
            [22.0240, 85.4220], [22.0265, 85.4315], [22.0230, 85.4435],
            [22.0155, 85.4470], [22.0080, 85.4410], [22.0065, 85.4285], [22.0120, 85.4195],
        ],
        "drill_points": [
            {"name": "Drill-JD-01", "lat": 22.0185, "lon": 85.4355, "depth": "88m", "status": "Completed"},
            {"name": "Drill-JD-02", "lat": 22.0145, "lon": 85.4305, "depth": "115m", "status": "In Progress"},
        ]
    },
    "srikakulam": {
        "name": "Srikakulam",
        "lat": 18.3000,
        "lon": 83.9000,
        "moisture": "21%",
        "ndvi": "0.53",
        "rainfall": "58 mm",
        "temp": "30.5°C",
        "polygon": [
            [18.3075, 83.8890], [18.3100, 83.8985], [18.3055, 83.9110],
            [18.2970, 83.9140], [18.2915, 83.9050], [18.2930, 83.8920], [18.2995, 83.8865],
        ],
        "drill_points": [
            {"name": "Drill-SK-01", "lat": 18.3025, "lon": 83.9025, "depth": "60m", "status": "Completed"},
        ]
    },
    "chhindwara": {
        "name": "Chhindwara",
        "lat": 22.0572,
        "lon": 78.9389,
        "moisture": "18%",
        "ndvi": "0.44",
        "rainfall": "47 mm",
        "temp": "32.0°C",
        "polygon": [
            [22.0645, 78.9270], [22.0670, 78.9365], [22.0625, 78.9490],
            [22.0540, 78.9520], [22.0485, 78.9430], [22.0500, 78.9300], [22.0565, 78.9245],
        ],
        "drill_points": [
            {"name": "Drill-CW-01", "lat": 22.0590, "lon": 78.9410, "depth": "75m", "status": "Completed"},
            {"name": "Drill-CW-02", "lat": 22.0550, "lon": 78.9365, "depth": "92m", "status": "Completed"},
        ]
    },
}


def render():
    st.markdown("## 🛰️ Satellite Intelligence")
    st.markdown("Search a mine → details appear on the left + Satellite map on the right")

    search = st.text_input(
        "Search Mine / Area (e.g. Balaghat, Ukwa, Dongri, Chikla...)",
        placeholder="Type mine name here..."
    )

    if search:
        key = search.lower().strip()
        found = None

        for k, v in MINE_DATA.items():
            if k in key or key in k:
                found = v
                break

        if found:
            st.success(f"**{found['name']} Mine** – Live Satellite Intelligence")

            # ========== SIDE BY SIDE LAYOUT ==========
            col1, col2 = st.columns([1, 2.2])   # Left: details | Right: map

            with col1:
                st.markdown("### 📊 Mine Details")
                st.markdown(f"""
                | Parameter              | Value              |
                |------------------------|--------------------|
                | **Soil Moisture**      | {found['moisture']} |
                | **NDVI**               | {found['ndvi']}    |
                | **7-day Rainfall**     | {found['rainfall']} |
                | **Land Temperature**   | {found['temp']}    |
                """)

                st.markdown("---")
                st.markdown("### 📍 Drill Points")
                for point in found["drill_points"]:
                    status_color = "🟢" if point["status"] == "Completed" else "🟠" if point["status"] == "In Progress" else "🔵"
                    st.markdown(f"{status_color} **{point['name']}**  \nDepth: {point['depth']}  \nStatus: {point['status']}")

            with col2:
                st.markdown(f"### 🛰️ Satellite View – {found['name']}")

                m = folium.Map(
                    location=[found["lat"], found["lon"]],
                    zoom_start=14,
                    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                    attr="Esri World Imagery"
                )

                # Realistic polygon
                folium.Polygon(
                    locations=found["polygon"],
                    color="#FFD700",
                    weight=3,
                    fill=True,
                    fill_color="#FFD700",
                    fill_opacity=0.30,
                    tooltip=f"{found['name']} Mine Boundary"
                ).add_to(m)

                # Center marker
                folium.Marker(
                    location=[found["lat"], found["lon"]],
                    tooltip=f"{found['name']} Mine Center",
                    icon=folium.Icon(color="red", icon="industry", prefix="fa")
                ).add_to(m)

                # Drill points
                for point in found["drill_points"]:
                    color = "green" if point["status"] == "Completed" else "orange" if point["status"] == "In Progress" else "blue"
                    folium.CircleMarker(
                        location=[point["lat"], point["lon"]],
                        radius=10,
                        color=color,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.95,
                        popup=f"<b>{point['name']}</b><br>Depth: {point['depth']}<br>Status: {point['status']}",
                        tooltip=f"{point['name']} | {point['depth']}"
                    ).add_to(m)

                st_folium(m, width=700, height=520, returned_objects=[])

                st.caption("Gold polygon = Mine boundary • Red marker = Center • Colored circles = Drill points")

        else:
            st.warning("No matching mine found. Try: Balaghat, Ukwa, Dongri, Chikla, Sandur, Bonai, Joda...")
    else:
        st.info("Type a mine name above. Details will appear on the left side of the map.")