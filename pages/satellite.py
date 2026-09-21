"""Geosatellite Analytics – clear cards, selectors & depth ladder (previous satellite kept)."""
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
    {"from": 0, "to": 1, "materials": "Soil, topsoil, organic / weathered material", "relevance": "Surface indicator", "tone": "#90caf9"},
    {"from": 1, "to": 1.5, "materials": "Manganese-bearing material (some Balaghat areas)", "relevance": "Mn mineralization (local)", "tone": "#66bb6a"},
    {"from": 1.5, "to": 5, "materials": "Laterite, limonite / goethite, weathered rock", "relevance": "Possible Fe–Mn indicator", "tone": "#aed581"},
    {"from": 5, "to": 10, "materials": "Weathered rock, phyllite / schist, quartz-bearing", "relevance": "Host-rock information", "tone": "#fff176"},
    {"from": 10, "to": 25, "materials": "Phyllite, quartz-mica schist, gneiss, Mn bands", "relevance": "Potential Mn zone", "tone": "#ffb74d"},
    {"from": 25, "to": 50, "materials": "Host rocks + mineralized bands / ore", "relevance": "Potential Mn zone", "tone": "#ff8a65"},
    {"from": 50, "to": 100, "materials": "Host rock + Mn ore / bands (UG)", "relevance": "Requires drill / core assay", "tone": "#e57373"},
    {"from": 100, "to": 150, "materials": "Host rock + possible ore body", "relevance": "Requires drill / core assay", "tone": "#ef5350"},
    {"from": 150, "to": 250, "materials": "UG host rock + ore zones", "relevance": "Requires drill / core assay", "tone": "#c62828"},
    {"from": 250, "to": 350, "materials": "Deeper UG workings / host rock", "relevance": "Mine-specific data", "tone": "#8e24aa"},
    {"from": 350, "to": 500, "materials": "Deep underground geological units", "relevance": "Mine-specific data", "tone": "#5e35b1"},
    {"from": 500, "to": 750, "materials": "Very deep UG rock (Balaghat shaft scale)", "relevance": "Not continuous Mn throughout", "tone": "#455a64"},
]

ORE_GRADES = [
    {"mine": "Balaghat", "type": "Ferro-grade jigged fines", "mn": 37, "p": 0.112, "sio2": 26, "fe": 6.5},
    {"mine": "Kandri", "type": "1st grade lump", "mn": 46, "p": 0.22, "sio2": 17, "fe": 5.2},
    {"mine": "Dongri Buzurg", "type": "Fines", "mn": 28, "p": 0.20, "sio2": 26, "fe": 12},
    {"mine": "Dongri Buzurg", "type": "Chemical grade", "mn": 39, "p": 0.20, "sio2": 18, "fe": 10},
    {"mine": "—", "type": "Silico-manganese grade", "mn": 25, "p": 0.28, "sio2": 36, "fe": 8.5},
    {"mine": "Tirodi", "type": "SM grade small", "mn": 25, "p": 0.35, "sio2": 45, "fe": 7.5},
    {"mine": "Sitapatore", "type": "25% SM grade", "mn": 25, "p": 0.40, "sio2": 38, "fe": 9},
]


def _inject_page_css():
    st.markdown("""
<style>
.gs-card {
    background: #fff; border: 1px solid #e0e7e4; border-radius: 12px;
    padding: 14px 16px; margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.gs-card h4 { margin: 0 0 6px 0; color: #00695c; font-size: 1rem; }
.gs-badge {
    display: inline-block; padding: 3px 10px; border-radius: 12px;
    font-size: 0.75rem; font-weight: 600; margin: 2px 4px 2px 0;
}
.gs-depth {
    font-size: 1.4rem; font-weight: 700; color: #00695c; margin: 4px 0;
}
.gs-muted { color: #78909c; font-size: 0.82rem; }
.gs-ladder-row {
    display: flex; align-items: stretch; margin-bottom: 6px; border-radius: 8px; overflow: hidden;
    border: 1px solid #eceff1;
}
.gs-ladder-depth {
    min-width: 88px; padding: 10px 8px; color: #fff; font-weight: 700;
    font-size: 0.78rem; text-align: center; display: flex; align-items: center; justify-content: center;
}
.gs-ladder-body { flex: 1; padding: 8px 12px; background: #fafafa; font-size: 0.84rem; }
.gs-bar-bg {
    background: #eceff1; border-radius: 8px; height: 12px; overflow: hidden; margin: 4px 0 10px 0;
}
.gs-bar-fill { height: 100%; border-radius: 8px; }
.gs-grade-title { font-weight: 700; color: #37474f; margin-bottom: 2px; }
</style>
""", unsafe_allow_html=True)


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
    st.caption("Search a mine/area for soil moisture, NDVI, rainfall and temperature.")

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
        st.info("Type a mine name above to see satellite parameters for that area.")

    with st.expander("Compare all regions (optional)"):
        sdf = _soil_dataframe()
        pick = st.selectbox(
            "Highlight region",
            ["(none)"] + sdf["Region"].tolist(),
            key="gs_region_pick",
        )
        cols = st.columns(2)
        for i, region in enumerate(sdf["Region"].tolist()):
            row = sdf[sdf["Region"] == region].iloc[0]
            border = "2px solid #00695c" if region == pick else "1px solid #e0e7e4"
            cols[i % 2].markdown(
                f"""
<div class="gs-card" style="border:{border}">
  <h4>{region}</h4>
  <span class="gs-badge" style="background:#e3f2fd;color:#1565c0;">Moisture {row['Soil Moisture %']:.0f}%</span>
  <span class="gs-badge" style="background:#e8f5e9;color:#2e7d32;">NDVI {row['NDVI']:.2f}</span>
  <span class="gs-badge" style="background:#e0f7fa;color:#00838f;">Rain {row['Rainfall (mm)']:.0f} mm</span>
  <span class="gs-badge" style="background:#fff3e0;color:#e65100;">Temp {row['Land Temp (°C)']:.1f}°C</span>
</div>
""",
                unsafe_allow_html=True,
            )


def _render_mine_depth_section():
    st.markdown("### Mine working levels")
    st.caption("Pick a mine to see its documented levels — no long tables.")

    mines = sorted({r["Mine"] for r in MINE_LEVELS})
    mine = st.selectbox("Select mine", mines, key="gs_mine_level")

    levels = [r for r in MINE_LEVELS if r["Mine"] == mine]
    depths = [r["Depth (m)"] for r in levels]
    deepest = min(depths)
    shallowest = max(depths)

    m1, m2, m3 = st.columns(3)
    m1.metric("Levels recorded", len(levels))
    m2.metric("Deepest level", f"{deepest} m")
    m3.metric("Shallowest level", f"{shallowest} m")

    for r in sorted(levels, key=lambda x: x["Depth (m)"]):
        d = r["Depth (m)"]
        label = f"{d} m" if d >= 0 else f"{d} m (below surface)"
        st.markdown(
            f"""
<div class="gs-card">
  <div class="gs-depth">{label}</div>
  <div><b>Material / ore:</b> {r['Material / ore']}</div>
  <div class="gs-muted">Source: {r['Data source']}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("##### Quick overview — deepest level per mine")
    overview = {}
    for r in MINE_LEVELS:
        name = r["Mine"]
        if name not in overview or r["Depth (m)"] < overview[name]:
            overview[name] = r["Depth (m)"]
    oc = st.columns(len(overview))
    for i, (name, d) in enumerate(sorted(overview.items(), key=lambda x: x[1])):
        oc[i].markdown(
            f"""
<div class="gs-card" style="text-align:center">
  <div class="gs-muted">{name}</div>
  <div class="gs-depth" style="font-size:1.15rem">{d} m</div>
</div>
""",
            unsafe_allow_html=True,
        )


def _render_depth_profile_section():
    st.markdown("### Depth → materials ladder")
    st.caption("Read top → bottom like a borehole strip. Colour = relative Mn interest (visual guide only).")

    zone = st.radio(
        "Focus depth range",
        ["All", "Near surface (0–50 m)", "Mid (50–250 m)", "Deep (250–750 m)"],
        horizontal=True,
        key="gs_depth_zone",
    )

    def in_zone(row):
        mid = (row["from"] + row["to"]) / 2
        if zone == "Near surface (0–50 m)":
            return mid <= 50
        if zone == "Mid (50–250 m)":
            return 50 < mid <= 250
        if zone == "Deep (250–750 m)":
            return mid > 250
        return True

    for row in DEPTH_PROFILE:
        if not in_zone(row):
            continue
        st.markdown(
            f"""
<div class="gs-ladder-row">
  <div class="gs-ladder-depth" style="background:{row['tone']}">{row['from']}–{row['to']} m</div>
  <div class="gs-ladder-body">
    <b>{row['relevance']}</b><br>
    <span class="gs-muted">{row['materials']}</span>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.caption(
        "Green / orange bands ≈ stronger Mn interest near known settings; "
        "deep purple/grey bands need mine-specific assay — not continuous ore."
    )


def _grade_bar(label, value, max_val, color):
    pct = max(0, min(100, (value / max_val) * 100))
    return f"""
<div style="font-size:0.8rem;color:#546e7a">{label}: <b style="color:#37474f">{value}</b></div>
<div class="gs-bar-bg"><div class="gs-bar-fill" style="width:{pct}%;background:{color}"></div></div>
"""


def _render_ore_grade_section():
    st.markdown("### Ore grade browser")
    st.caption("Choose one product — see Mn, Fe, SiO₂, P as simple bars.")

    labels = [f"{g['mine']} · {g['type']}" for g in ORE_GRADES]
    choice = st.selectbox("Ore product", labels, key="gs_ore_pick")
    g = ORE_GRADES[labels.index(choice)]

    mn_color = "#2e7d32" if g["mn"] >= 40 else "#f9a825" if g["mn"] >= 30 else "#c62828"
    st.markdown(
        f"""
<div class="gs-card">
  <div class="gs-grade-title">{g['mine']} — {g['type']}</div>
  <div class="gs-depth" style="color:{mn_color}">{g['mn']}% Mn</div>
  <span class="gs-badge" style="background:#e8f5e9;color:#2e7d32;">Manganese</span>
  <span class="gs-badge" style="background:#fff3e0;color:#e65100;">Fe {g['fe']}%</span>
  <span class="gs-badge" style="background:#e3f2fd;color:#1565c0;">SiO₂ {g['sio2']}%</span>
  <span class="gs-badge" style="background:#fce4ec;color:#ad1457;">P {g['p']}%</span>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        _grade_bar("Mn %", g["mn"], 50, "#00695c")
        + _grade_bar("Fe %", g["fe"], 15, "#e65100")
        + _grade_bar("SiO₂ %", g["sio2"], 50, "#1565c0")
        + _grade_bar("P %", g["p"], 0.5, "#ad1457"),
        unsafe_allow_html=True,
    )

    st.markdown("##### All products at a glance (Mn only)")
    ranked = sorted(ORE_GRADES, key=lambda x: -x["mn"])
    chip_html = ""
    for item in ranked:
        col = "#2e7d32" if item["mn"] >= 40 else "#f9a825" if item["mn"] >= 30 else "#c62828"
        chip_html += (
            f'<span class="gs-badge" style="background:#f5f5f5;color:{col};border:1px solid #e0e0e0">'
            f'{item["mine"]}: {item["mn"]}% Mn</span> '
        )
    st.markdown(chip_html, unsafe_allow_html=True)

    best = max(ORE_GRADES, key=lambda x: x["mn"])
    st.success(f"Highest Mn in this set: **{best['mine']} — {best['type']} ({best['mn']}%)**")


def render():
    _inject_page_css()
    st.markdown("## Geosatellite Analytics")
    st.markdown(
        "Satellite surface context · mine working depths · depth–material ladder · ore grade browser."
    )

    tabs = st.tabs([
        "📡 Satellite parameters",
        "⛏️ Mine depths",
        "🪨 Depth ladder",
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