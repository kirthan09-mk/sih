"""Geological Insights page."""
import streamlit as st

GEO_DATA = {
    "balaghat": {
        "name": "Balaghat",
        "main": "Sub-surface dominant",
        "surface": ["Black manganese outcrops", "Laterite cover", "Old workings", "Shear zones"],
        "subsurface": ["High IP chargeability", "Low resistivity", "Magnetic anomalies", "Gravity highs", "Deep drilling"],
        "notes": "One of the deepest mines. Sub-surface geophysics + drilling are primary.",
        "mn_grade": "42-48%",
        "depth": "Up to 380m+"
    },
    "ukwa": {
        "name": "Ukwa",
        "main": "Sub-surface dominant",
        "surface": ["Laterite cover", "Old workings", "Shear zones"],
        "subsurface": ["High IP chargeability", "Low resistivity", "Magnetic anomalies", "Underground mapping"],
        "notes": "Strong geophysical response confirmed by underground drilling.",
        "mn_grade": "38-45%",
        "depth": "250-320m"
    },
    "dongri": {
        "name": "Dongri Buzurg",
        "main": "Surface dominant",
        "surface": ["Black manganese outcrops", "Prominent exposures", "Old workings", "Laterite cover"],
        "subsurface": ["Shallow drilling", "Limited geophysics"],
        "notes": "Classic surface-identified open-cast deposit.",
        "mn_grade": "40-46%",
        "depth": "Shallow (Open cast)"
    },
    "chikla": {
        "name": "Chikla",
        "main": "Both (Balanced)",
        "surface": ["Black manganese outcrops", "Laterite cover", "Shear zones"],
        "subsurface": ["High IP chargeability", "Low resistivity", "Magnetic anomalies"],
        "notes": "Good balance of surface and sub-surface signatures.",
        "mn_grade": "36-43%",
        "depth": "180-280m"
    },
    "nagpur": {
        "name": "Nagpur Region",
        "main": "Surface dominant",
        "surface": ["Laterite cover", "Old workings", "Shear zones"],
        "subsurface": ["Limited geophysical data"],
        "notes": "Mostly surface geological mapping.",
        "mn_grade": "32-40%",
        "depth": "Shallow to moderate"
    },
    "sandur": {
        "name": "Sandur",
        "main": "Surface dominant",
        "surface": ["Black manganese outcrops", "Laterite cover", "Prominent exposures"],
        "subsurface": ["Limited drilling"],
        "notes": "Strong surface indicators.",
        "mn_grade": "35-42%",
        "depth": "Shallow"
    },
    "bonai": {
        "name": "Bonai",
        "main": "Both",
        "surface": ["Laterite cover", "Old workings"],
        "subsurface": ["Magnetic anomalies", "Gravity highs"],
        "notes": "Mix of surface and geophysical methods.",
        "mn_grade": "34-41%",
        "depth": "Moderate"
    },
    "joda": {
        "name": "Joda",
        "main": "Surface dominant",
        "surface": ["Black manganese outcrops", "Laterite cover", "Old workings"],
        "subsurface": ["Limited data"],
        "notes": "Primarily surface identification.",
        "mn_grade": "38-44%",
        "depth": "Shallow to moderate"
    },
    "srikakulam": {
        "name": "Srikakulam",
        "main": "Surface dominant",
        "surface": ["Laterite cover", "Shear zones"],
        "subsurface": ["Very limited data"],
        "notes": "Mostly surface-based.",
        "mn_grade": "30-38%",
        "depth": "Shallow"
    },
    "chhindwara": {
        "name": "Chhindwara",
        "main": "Both",
        "surface": ["Laterite cover", "Old workings"],
        "subsurface": ["High IP chargeability", "Magnetic anomalies"],
        "notes": "Balanced surface + sub-surface approach.",
        "mn_grade": "33-40%",
        "depth": "Moderate"
    },
}


def render():
    st.markdown("## Geological Insights")

    # Header box
    st.markdown("""
    <div style="background:#f0f7f4; padding:18px; border-radius:12px; border-left:6px solid #00695c; margin-bottom: 25px;">
    <b>Sausar Group – Central Indian Manganese Belt</b><br>
    Main host → <b>Mansar Formation</b> | Rock type → <b>Gondite</b>
    </div>
    """, unsafe_allow_html=True)

    # ========== SEARCH SINGLE MINE ==========
    st.markdown("### 🔍 Single Mine Analysis")
    search = st.text_input("Search Mine Name", placeholder="e.g. Balaghat, Dongri, Ukwa...")

    if search:
        key = search.lower().strip()
        found = None
        for k, v in GEO_DATA.items():
            if k in key or key in k:
                found = v
                break

        if found:
            st.success(f"**{found['name']} Mine**")

            if "Surface dominant" in found["main"]:
                color, label = "#2e7d32", "🌿 Primarily Surface Indicators"
            elif "Sub-surface dominant" in found["main"]:
                color, label = "#1565c0", "⛏️ Primarily Sub-surface Indicators"
            else:
                color, label = "#6a1b9a", "🟣 Both Surface + Sub-surface"

            st.markdown(f"""
            <div style="background:{color}15; padding:14px 18px; border-radius:10px; border-left:5px solid {color}; margin-bottom:20px;">
                <b style="color:{color}; font-size:17px;">{label}</b>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("Mn Grade", found["mn_grade"])
            c2.metric("Working Depth", found["depth"])
            c3.metric("Method", found["main"].split()[0])

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🌿 Surface Indicators")
                for item in found["surface"]:
                    st.markdown(f"- {item}")
            with col2:
                st.markdown("#### ⛏️ Sub-surface Indicators")
                for item in found["subsurface"]:
                    st.markdown(f"- {item}")

            st.info(f"**Note:** {found['notes']}")
        else:
            st.warning("Mine not found. Try Balaghat, Ukwa, Dongri, Chikla...")

    st.markdown("---")

    # ========== COMPARISON TABLE ==========
    st.markdown("### 📊 Mine Comparison Table")
    st.caption("Select 2 or 3 mines to compare side-by-side")

    mine_options = list(GEO_DATA.keys())
    selected = st.multiselect(
        "Select mines to compare",
        options=mine_options,
        default=["balaghat", "dongri"],
        format_func=lambda x: GEO_DATA[x]["name"]
    )

    if len(selected) >= 2:
        # Build comparison data
        comparison_data = {
            "Parameter": ["Identification Method", "Mn Grade", "Working Depth", "Main Strength"]
        }

        for mine_key in selected:
            mine = GEO_DATA[mine_key]
            comparison_data[mine["name"]] = [
                mine["main"],
                mine["mn_grade"],
                mine["depth"],
                "Surface" if "Surface" in mine["main"] else "Sub-surface" if "Sub-surface" in mine["main"] else "Balanced"
            ]

        st.dataframe(comparison_data, use_container_width=True, hide_index=True)

        # Detailed indicator comparison
        st.markdown("#### Detailed Indicators Comparison")
        cols = st.columns(len(selected))
        for idx, mine_key in enumerate(selected):
            mine = GEO_DATA[mine_key]
            with cols[idx]:
                st.markdown(f"**{mine['name']}**")
                st.markdown("**Surface:**")
                for s in mine["surface"][:3]:
                    st.caption(f"• {s}")
                st.markdown("**Sub-surface:**")
                for s in mine["subsurface"][:3]:
                    st.caption(f"• {s}")
    else:
        st.info("Select at least 2 mines to see the comparison table.")