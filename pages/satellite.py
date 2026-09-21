"""Geosatellite Analytics – satellite params + mine depth / ore grade analytics."""
import pandas as pd
import streamlit as st

# ─── Existing regional satellite data (unchanged) ───
SOIL_DATA = {
    "balaghat": {"moisture": "19%", "ndvi": "0.48", "rainfall": "52 mm", "temp": "31.8°C"},
    "ukwa": {"moisture": "18%", "ndvi": "0.45", "rainfall": "48 mm", "temp": "32.1°C"},
    "dongri": {"moisture": "17%", "ndvi": "0.41", "rainfall": "45 mm", "temp": "33.0°C"},
    "chikla": {"moisture": "16%", "ndvi": "0.39", "rainfall": "43 mm", "temp": "32.7°C"},
    "nagpur": {"moisture": "15%", "ndvi": "0.37", "rainfall": "40 mm", "temp": "33.5°C"},
    "sandur": {"moisture": "14%", "ndvi": "0.34", "rainfall": "38 mm", "temp": "34.2°C"},
    "bonai": {"moisture": "20%", "ndvi": "0.51", "rainfall": "55 mm", "temp": "30.9°C"},
    "joda": {"moisture": "19%", "ndvi": "0.49", "rainfall": "53 mm", "temp": "31.2°C"},
    "srikakulam": {"moisture": "21%", "ndvi": "0.53", "rainfall": "58 mm", "temp": "30.5°C"},
    "chhindwara": {"moisture": "18%", "ndvi": "0.44", "rainfall": "47 mm", "temp": "32.0°C"},
}

MINE_LEVELS = [
    {"Mine": "Chikla", "Depth (m)": -230, "Material / ore": "Manganiferous / ore zone", "Data source": "Assay data"},
    {"Mine": "Chikla", "Depth (m)": -470, "Material / ore": "Manganiferous rock / ore body", "Data source": "Assay data"},
    {"Mine": "Kandri", "Depth (m)": -350, "Material / ore": "Ore body", "Data source": "Assay data"},
    {"Mine": "Munsar", "Depth (m)": 70, "Material / ore": "Geological / working level", "Data source": "Assay data"},
    {"Mine": "Munsar", "Depth (m)": -30, "Material / ore": "Geological / working level", "Data source": "Assay data"},
    {"Mine": "Munsar", "Depth (m)": -230, "Material / ore": "Geological / working level", "Data source": "Assay data"},
    {"Mine": "Balaghat", "Depth (m)": -750, "Material / ore": "Underground exploration / workings", "Data source": "Drill / core assay"},
]

DEPTH_PROFILE = [
    {"Depth from (m)": 0, "Depth to (m)": 1, "Materials / minerals": "Soil, topsoil, organic / weathered material", "Mn relevance": "Surface indicator"},
    {"Depth from (m)": 1, "Depth to (m)": 1.5, "Materials / minerals": "Manganese-bearing material (some Balaghat areas)", "Mn relevance": "Mn mineralization (local)"},
    {"Depth from (m)": 1.5, "Depth to (m)": 5, "Materials / minerals": "Laterite, limonite / goethite, weathered rock, soil", "Mn relevance": "Possible Fe–Mn indicator"},
    {"Depth from (m)": 5, "Depth to (m)": 10, "Materials / minerals": "Weathered rock, phyllite / schist, quartz-bearing material", "Mn relevance": "Host-rock information"},
    {"Depth from (m)": 10, "Depth to (m)": 25, "Materials / minerals": "Phyllite, quartz-mica schist, gneiss, Mn bands where present", "Mn relevance": "Potential Mn zone"},
    {"Depth from (m)": 25, "Depth to (m)": 50, "Materials / minerals": "Host rocks + mineralized bands / ore (structure-dependent)", "Mn relevance": "Potential Mn zone"},
    {"Depth from (m)": 50, "Depth to (m)": 100, "Materials / minerals": "Host rock, quartz-bearing rock, Mn ore / bands (UG deposits)", "Mn relevance": "Requires drill / core assay"},
    {"Depth from (m)": 100, "Depth to (m)": 150, "Materials / minerals": "Host rock + possible ore body", "Mn relevance": "Requires drill / core assay"},
    {"Depth from (m)": 150, "Depth to (m)": 250, "Materials / minerals": "Underground host rock + ore zones (suitable deposits)", "Mn relevance": "Requires drill / core assay"},
    {"Depth from (m)": 250, "Depth to (m)": 350, "Materials / minerals": "Deeper UG workings / host rock (some MOIL mines)", "Mn relevance": "Mine-specific data"},
    {"Depth from (m)": 350, "Depth to (m)": 500, "Materials / minerals": "Deep underground geological units", "Mn relevance": "Mine-specific data"},
    {"Depth from (m)": 500, "Depth to (m)": 750, "Materials / minerals": "Very deep UG rock (Balaghat shaft scale)", "Mn relevance": "Not continuous Mn throughout"},
]

ORE_GRADES = [
    {"Mine / source": "Balaghat", "Ore type": "Ferro-grade jigged fines", "Mn %": 37, "P %": 0.112, "SiO₂ %": 26, "Fe %": 6.5},
    {"Mine / source": "Kandri", "Ore type": "1st grade lump", "Mn %": 46, "P %": 0.22, "SiO₂ %": 17, "Fe %": 5.2},
    {"Mine / source": "Dongri Buzurg", "Ore type": "Fines", "Mn %": 28, "P %": 0.20, "SiO₂ %": 26, "Fe %": 12},
    {"Mine / source": "Dongri Buzurg", "Ore type": "Chemical grade", "Mn %": 39, "P %": 0.20, "SiO₂ %": 18, "Fe %": 10},
    {"Mine / source": "—", "Ore type": "Silico-manganese grade", "Mn %": 25, "P %": 0.28, "SiO₂ %": 36, "Fe %": 8.5},
    {"Mine / source": "Tirodi", "Ore type": "SM grade small", "Mn %": 25, "P %": 0.35, "SiO₂ %": 45, "Fe %": 7.5},
    {"Mine / source": "Sitapatore", "Ore type": "25% SM grade", "Mn %": 25, "P %": 0.40, "SiO₂ %": 38, "Fe %": 9},
]


def _soil_dataframe() -> pd.DataFrame:
    rows = []
    for name, v in SOIL_DATA.items():
        rows.append({
            "Region": name.title(),
            "Soil Moisture %": float(v["moisture"].replace("%", "")),
            "NDVI": float(v["ndvi"]),
            "Rainfall (mm)": float(v["rainfall"].replace(" mm", "")),
            "Land Temp (°C)": float(v["temp"].replace("°C", "")),
        })
    return pd.DataFrame(rows).sort_values("Region")


def _render_existing_satellite_section():
    st.markdown("### Regional satellite parameters")
    st.markdown("Search any mine to see soil moisture and related data for that area.")

    search = st.text_input("Search Mine / Area (e.g. Balaghat, Dongri, Srikakulam, Sandur)")

    if search:
        key = search.lower().strip()
        found = False
        for k, v in SOIL_DATA.items():
            if k in key or key in k:
                st.success(f"Data for **{search.title()}** region")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Soil Moisture", v["moisture"])
                c2.metric("NDVI", v["ndvi"])
                c3.metric("7-day Rainfall", v["rainfall"])
                c4.metric("Land Temp", v["temp"])
                found = True
                break
        if not found:
            st.warning(
                "No matching mine found. Try: Balaghat, Dongri, Ukwa, Sandur, "
                "Srikakulam, Bonai, Joda..."
            )
    else:
        st.info("Type a mine name above to see detailed satellite parameters for that area.")

    st.markdown("#### Regional comparison")
    sdf = _soil_dataframe()
    tab1, tab2, tab3 = st.tabs(["Soil Moisture & NDVI", "Rainfall & Temperature", "Data table"])

    with tab1:
        a, b = st.columns(2)
        with a:
            st.markdown("##### Soil Moisture (%)")
            st.bar_chart(sdf.set_index("Region")[["Soil Moisture %"]], height=280, color="#1565c0")
        with b:
            st.markdown("##### NDVI")
            st.bar_chart(sdf.set_index("Region")[["NDVI"]], height=280, color="#2e7d32")

    with tab2:
        a, b = st.columns(2)
        with a:
            st.markdown("##### 7-day Rainfall (mm)")
            st.bar_chart(sdf.set_index("Region")[["Rainfall (mm)"]], height=280, color="#00838f")
        with b:
            st.markdown("##### Land Temperature (°C)")
            st.bar_chart(sdf.set_index("Region")[["Land Temp (°C)"]], height=280, color="#e65100")

    with tab3:
        st.dataframe(
            sdf.style.format({
                "Soil Moisture %": "{:.0f}",
                "NDVI": "{:.2f}",
                "Rainfall (mm)": "{:.0f}",
                "Land Temp (°C)": "{:.1f}",
            }),
            use_container_width=True,
            hide_index=True,
        )


def _render_mine_depth_section():
    st.markdown("### Mine working levels & depth")
    st.caption("Documented underground / working levels (assay / drill context).")

    levels = pd.DataFrame(MINE_LEVELS)
    chart_df = levels.copy()
    chart_df["Depth magnitude (m)"] = chart_df["Depth (m)"].abs()
    chart_df["Label"] = chart_df["Mine"] + " (" + chart_df["Depth (m)"].astype(str) + " m)"

    c1, c2 = st.columns([1.35, 1])
    with c1:
        st.markdown("##### Working depth by mine level")
        st.bar_chart(chart_df.set_index("Label")[["Depth magnitude (m)"]], height=320, color="#00695c")
        st.caption("Bar length = |depth|. Munsar +70 m is above reference; others below surface.")
    with c2:
        st.markdown("##### Level register")
        st.dataframe(levels, use_container_width=True, hide_index=True)

    span = levels.groupby("Mine")["Depth (m)"].agg(min_depth="min", max_depth="max").reset_index()
    span["Vertical span (m)"] = (span["max_depth"] - span["min_depth"]).abs()
    st.markdown("##### Vertical span per mine")
    st.bar_chart(span.set_index("Mine")[["Vertical span (m)"]], height=240, color="#ff6d00")


def _render_depth_profile_section():
    st.markdown("### Depth vs materials / minerals profile")
    st.caption("Generalised profile 0–750 m. Deeper bands need drill/core assay — not continuous Mn ore.")

    profile = pd.DataFrame(DEPTH_PROFILE)
    profile["Layer thickness (m)"] = profile["Depth to (m)"] - profile["Depth from (m)"]
    profile["Layer"] = profile["Depth from (m)"].astype(str) + "–" + profile["Depth to (m)"].astype(str) + " m"

    rel_map = {
        "Surface indicator": 1,
        "Mn mineralization (local)": 5,
        "Possible Fe–Mn indicator": 3,
        "Host-rock information": 2,
        "Potential Mn zone": 4,
        "Requires drill / core assay": 3,
        "Mine-specific data": 2,
        "Not continuous Mn throughout": 1,
    }
    profile["Relevance index"] = profile["Mn relevance"].map(rel_map).fillna(1)

    t1, t2 = st.tabs(["Layer thickness by depth band", "Mn relevance index by depth"])
    with t1:
        st.bar_chart(profile.set_index("Layer")[["Layer thickness (m)"]], height=340, color="#1565c0")
        st.caption("Thicker bars = wider depth interval, not higher ore grade.")
    with t2:
        st.bar_chart(profile.set_index("Layer")[["Relevance index"]], height=340, color="#2e7d32")
        st.caption("Visual rank of stated Mn relevance (not a measured grade).")

    st.markdown("##### Full depth–material table")
    st.dataframe(
        profile[["Depth from (m)", "Depth to (m)", "Materials / minerals", "Mn relevance", "Layer thickness (m)"]],
        use_container_width=True,
        hide_index=True,
    )


def _render_ore_grade_section():
    st.markdown("### Ore grade composition")
    st.caption("Sample grade snapshots (Mn, P, SiO₂, Fe) by mine / product type.")

    grades = pd.DataFrame(ORE_GRADES)
    grades["Label"] = grades["Mine / source"] + " – " + grades["Ore type"]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Highest Mn %", f"{grades['Mn %'].max()}%", grades.loc[grades["Mn %"].idxmax(), "Mine / source"])
    k2.metric("Lowest Mn %", f"{grades['Mn %'].min()}%")
    k3.metric("Avg Mn %", f"{grades['Mn %'].mean():.1f}%")
    k4.metric("Samples", str(len(grades)))

    g1, g2 = st.columns(2)
    with g1:
        st.markdown("##### Mn % by product")
        st.bar_chart(grades.set_index("Label")[["Mn %"]], height=320, color="#00695c")
    with g2:
        st.markdown("##### Fe % by product")
        st.bar_chart(grades.set_index("Label")[["Fe %"]], height=320, color="#e65100")

    g3, g4 = st.columns(2)
    with g3:
        st.markdown("##### SiO₂ % by product")
        st.bar_chart(grades.set_index("Label")[["SiO₂ %"]], height=280, color="#1565c0")
    with g4:
        st.markdown("##### P % by product")
        st.bar_chart(grades.set_index("Label")[["P %"]], height=280, color="#f9a825")

    st.markdown("##### Multi-element comparison (Mn · Fe · SiO₂)")
    st.bar_chart(grades.set_index("Label")[["Mn %", "Fe %", "SiO₂ %"]], height=340)

    st.markdown("##### Grade register")
    st.dataframe(
        grades[["Mine / source", "Ore type", "Mn %", "P %", "SiO₂ %", "Fe %"]],
        use_container_width=True,
        hide_index=True,
    )


def render():
    st.markdown("## Geosatellite Analytics")
    st.markdown(
        "Satellite indicators for surface context, plus **mine depth levels**, "
        "**depth–material profiles**, and **ore grade composition**."
    )

    tabs = st.tabs([
        "📡 Satellite parameters",
        "⛏️ Mine depths",
        "🪨 Depth–mineral profile",
        "📊 Ore grades",
    ])
    with tabs[0]:
        _render_existing_satellite_section()
    with tabs[1]:
        _render_mine_depth_section()
    with tabs[2]:
        _render_depth_profile_section()
    with tabs[3]:
        _render_ore_grade_section()