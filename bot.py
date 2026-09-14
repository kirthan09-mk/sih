"""MOIL AI chatbot response logic."""
import streamlit as st


def get_bot_response(user_input):
    text = user_input.lower().strip()

    # ---------- MAP VIEW SWITCH ----------
    if any(w in text for w in ["satellite", "sat view", "satellite view"]):
        st.session_state.map_view = "Satellite"
        return "Switched to **Satellite** view.", None, None
    if any(w in text for w in ["terrain", "topo", "topographic"]):
        st.session_state.map_view = "Terrain"
        return "Switched to **Terrain** view.", None, None
    if any(w in text for w in ["light", "grey", "gray", "light map"]):
        st.session_state.map_view = "Light Map"
        return "Switched to **Light Map** view.", None, None
    if any(w in text for w in ["street", "osm", "street map"]):
        st.session_state.map_view = "Street Map"
        return "Switched to **Street Map** view.", None, None

    # ---------- MINE / STATE ZOOM + OPEN POPUP ----------
    zoom_map = {
        "balaghat": ("Balaghat Belt (MOIL – Largest)", [21.82, 80.18], 12),
        "ukwa": ("Ukwa Mine (MOIL)", [21.95, 80.45], 13),
        "tirodi": ("Tirodi Mine (MOIL)", [21.70, 79.72], 13),
        "sitapatore": ("Sitapatore Mine (MOIL)", [21.68, 79.67], 13),
        "chhindwara": ("Chhindwara (MP)", [22.05, 78.95], 12),
        "dongri": ("Dongri Buzurg (MOIL)", [21.35, 79.85], 13),
        "chikla": ("Chikla Mine (MOIL)", [21.40, 79.70], 13),
        "kandri": ("Kandri–Munsar Cluster", [21.45, 79.05], 12),
        "munsar": ("Kandri–Munsar Cluster", [21.45, 79.05], 12),
        "nagpur": ("Nagpur–Bhandara Cluster", [21.25, 79.15], 11),
        "bhandara": ("Nagpur–Bhandara Cluster", [21.25, 79.15], 11),
        "sandur": ("Sandur Belt (Karnataka)", [15.10, 76.55], 11),
        "bonai": ("Bonai–Keonjhar (Odisha)", [21.85, 85.25], 11),
        "keonjhar": ("Bonai–Keonjhar (Odisha)", [21.85, 85.25], 11),
        "joda": ("Joda–Barbil (Odisha)", [22.05, 85.45], 12),
        "barbil": ("Joda–Barbil (Odisha)", [22.05, 85.45], 12),
        "srikakulam": ("Srikakulam (AP)", [18.30, 83.90], 11),
        "maharashtra": (None, [21.4, 79.5], 9),
        "madhya pradesh": (None, [21.9, 79.9], 9),
        "odisha": (None, [21.9, 85.3], 9),
        "karnataka": (None, [15.1, 76.5], 9),
        "andhra": (None, [18.3, 83.9], 9),
    }

    for key, (mine_name, center, zoom) in zoom_map.items():
        if key in text:
            st.session_state.open_popup_mine = mine_name
            return f"Zooming to **{key.title()}**...", center, zoom

    # ---------- SURFACE INDICATORS ----------
    if any(w in text for w in ["surface indicator", "surface indicators", "surface sign", "surface signs", "outcrop", "laterite", "old working"]):
        return """**Surface Indicators** of manganese mineralization:

• Black manganese outcrops  
• Laterite cover  
• Old workings / pits  
• Shear zones  

These are important visual clues used during field exploration.""", None, None

    # ---------- SUB-SURFACE INDICATORS ----------
    if any(w in text for w in ["sub-surface", "subsurface", "geophysical", "ip", "chargeability", "resistivity", "magnetic anomaly", "gravity"]):
        return """**Sub-surface Indicators**:

• High IP (Induced Polarization) chargeability  
• Low resistivity zones  
• Magnetic anomalies  
• Gravity highs  

These help identify hidden manganese bodies below the surface.""", None, None

    # ---------- GEOLOGY ----------
    if any(w in text for w in ["geology", "geological", "gondite", "sausar", "mansar", "host rock"]):
        return """**Geological Setting**:

• Belongs to **Sausar Group** (Central Indian Manganese Belt)  
• Main host formation → **Mansar Formation**  
• Host rock → **Gondite**  

This is the primary geological setup of MOIL’s manganese deposits.""", None, None

    # ---------- PRODUCTION ----------
    if any(w in text for w in ["production", "produce", "output", "lakh tonne", "production data"]):
        return """**MOIL Production Performance**:

• **FY 2024-25** → **18.03 lakh tonnes** (Highest ever)  
• FY 2023-24 → 17.56 lakh tonnes  
• FY 2022-23 → 13.00 lakh tonnes  

MOIL contributes approximately **45–50%** of India’s total manganese ore production.""", None, None

    # ---------- SHORTFALL / CHALLENGES ----------
    if any(w in text for w in ["shortfall", "shortage", "challenge", "problem", "issue", "deficit"]):
        return """**Production Challenges & Shortfalls**:

• Weather disruptions during monsoon  
• Temporary operational constraints  
• Logistics and evacuation issues in some areas  
• Grade variation in some mines  

Despite these, MOIL achieved record production in FY 2024-25.""", None, None

    # ---------- RAINFALL / WEATHER ----------
    if any(w in text for w in ["rainfall", "rain", "weather", "monsoon", "precipitation"]):
        return """**Rainfall & Weather Conditions**:

• Recent 7-day rainfall in core belt → **35–55 mm**  
• Highest rainfall occurs during monsoon season  
• Heavy rain affects mine drainage, slope stability and operations  

Weather monitoring is important for safe mining operations.""", None, None

    # ---------- SOIL MOISTURE ----------
    if any(w in text for w in ["soil moisture", "moisture", "soil water"]):
        return """**Soil Moisture**:

• Average in main manganese belt → **15–22%**  
• Higher moisture can affect drilling performance and slope stability  
• Data source: SMAP / satellite model data  

Useful for operational planning and geotechnical assessment.""", None, None

    # ---------- NDVI ----------
    if any(w in text for w in ["ndvi", "vegetation", "vegetation index", "green cover"]):
        return """**NDVI (Normalized Difference Vegetation Index)**:

• Typical range around mines → **0.35 – 0.55**  
• Higher NDVI = denser vegetation  
• Helps identify disturbed land and vegetation health near mining areas""", None, None

    # ---------- EQUIPMENT ----------
    if any(w in text for w in ["equipment", "shovel", "dumper", "drill", "jumbo", "loader", "fleet"]):
        return """**Mining Equipment Fleet**:

• Hydraulic Shovels  
• Dumpers / Haul trucks  
• Jumbo Drills  
• Loaders (LHDs)  

Improved equipment efficiency has contributed to rising production levels.""", None, None

    # ---------- DRILL TARGETS / COLORS ----------
    if any(w in text for w in ["drill target", "green dot", "yellow dot", "red dot", "confidence", "high confidence"]):
        return """**Drill Targets Colour Meaning**:

• 🟢 **Green** → High Confidence (> 85%)  
• 🟡 **Yellow** → Medium Confidence (70–85%)  
• 🔴 **Red** → Lower Confidence (< 70%)  

These are AI-suggested high-potential exploration points.""", None, None

    # ---------- MOIL ----------
    if any(w in text for w in ["moil", "what is moil", "about moil", "moil limited"]):
        return """**MOIL Limited**:

• India’s largest manganese ore producer  
• Miniratna Central Public Sector Enterprise under Ministry of Steel  
• Operates underground and opencast mines mainly in Madhya Pradesh and Maharashtra  
• Major mines: Balaghat, Ukwa, Dongri Buzurg, Chikla, Tirodi etc.""", None, None

    # ---------- HELP ----------
    if any(w in text for w in ["help", "what can you do", "commands", "how to use"]):
        return """I can help you with:

• Zoom to any mine or state  
• Switch map views  
• Surface & Sub-surface indicators  
• Geology (Sausar Group, Gondite)  
• Production data  
• Rainfall, Soil Moisture, NDVI  
• Equipment information  
• Drill target colours  

Just ask naturally!""", None, None

    # ---------- GREETINGS ----------
    if any(w in text for w in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return "Hello! I am the **MOIL AI Assistant**. Ask me about mines, geology, production, weather, soil moisture, NDVI or anything on this platform.", None, None

    # ---------- DEFAULT ----------
    return """I can answer questions about:

• Mines & locations  
• Surface / Sub-surface indicators  
• Geology  
• Production & shortfalls  
• Rainfall, Soil Moisture, NDVI  
• Equipment  
• Map features  

Please try asking more specifically.""", None, None