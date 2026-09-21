"""Production Prediction Analysis – Fully Redesigned + Fixed
Modern UI + Premium Graphs + 10-Year Forecast
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ------------------------------------------------------------------
# Data
# ------------------------------------------------------------------
TOTALS = {
    "FY21": 11.44, "FY22": 12.31, "FY23": 13.02, "FY24": 17.56, "FY25": 18.03,
}

MINE_SPLIT = {
    "FY21": {
        "Balaghat (Madhya Pradesh)": 3.80, "Dongri Buzurg (Maharashtra)": 1.65,
        "Chikla (Maharashtra)": 1.20, "Ukwa (Madhya Pradesh)": 1.10,
        "Tirodi (Madhya Pradesh)": 0.95, "Kandri (Maharashtra)": 0.85,
        "Munsar (Maharashtra)": 0.70, "Gumgaon (Maharashtra)": 0.55,
        "Beldongri (Maharashtra)": 0.40, "Sitapatore (Madhya Pradesh)": 0.24
    },
    "FY22": {
        "Balaghat (Madhya Pradesh)": 4.10, "Dongri Buzurg (Maharashtra)": 1.75,
        "Chikla (Maharashtra)": 1.30, "Ukwa (Madhya Pradesh)": 1.15,
        "Tirodi (Madhya Pradesh)": 1.00, "Kandri (Maharashtra)": 0.90,
        "Munsar (Maharashtra)": 0.75, "Gumgaon (Maharashtra)": 0.60,
        "Beldongri (Maharashtra)": 0.45, "Sitapatore (Madhya Pradesh)": 0.31
    },
    "FY23": {
        "Balaghat (Madhya Pradesh)": 4.30, "Dongri Buzurg (Maharashtra)": 1.85,
        "Chikla (Maharashtra)": 1.40, "Ukwa (Madhya Pradesh)": 1.25,
        "Tirodi (Madhya Pradesh)": 1.05, "Kandri (Maharashtra)": 0.95,
        "Munsar (Maharashtra)": 0.80, "Gumgaon (Maharashtra)": 0.65,
        "Beldongri (Maharashtra)": 0.48, "Sitapatore (Madhya Pradesh)": 0.29
    },
    "FY24": {
        "Balaghat (Madhya Pradesh)": 5.85, "Dongri Buzurg (Maharashtra)": 2.40,
        "Chikla (Maharashtra)": 1.90, "Ukwa (Madhya Pradesh)": 1.70,
        "Tirodi (Madhya Pradesh)": 1.45, "Kandri (Maharashtra)": 1.30,
        "Munsar (Maharashtra)": 1.05, "Gumgaon (Maharashtra)": 0.90,
        "Beldongri (Maharashtra)": 0.65, "Sitapatore (Madhya Pradesh)": 0.36
    },
    "FY25": {
        "Balaghat (Madhya Pradesh)": 6.00, "Dongri Buzurg (Maharashtra)": 2.45,
        "Chikla (Maharashtra)": 1.95, "Ukwa (Madhya Pradesh)": 1.75,
        "Tirodi (Madhya Pradesh)": 1.50, "Kandri (Maharashtra)": 1.35,
        "Munsar (Maharashtra)": 1.10, "Gumgaon (Maharashtra)": 0.95,
        "Beldongri (Maharashtra)": 0.68, "Sitapatore (Madhya Pradesh)": 0.30
    },
}

YEARS = list(TOTALS.keys())
FUTURE_YEARS = [f"FY{str(i).zfill(2)}" for i in range(26, 36)]
ALL_MINES = list(MINE_SPLIT["FY25"].keys())

CAPACITY_PROJECTS = {
    "Balaghat (Madhya Pradesh)": [
        {"year": "FY28", "extra": 1.20, "note": "High-speed shaft + deeper levels"},
        {"year": "FY30", "extra": 0.80, "note": "Further deepening"},
        {"year": "FY33", "extra": 0.60, "note": "Long-term expansion"},
    ],
    "Dongri Buzurg (Maharashtra)": [
        {"year": "FY28", "extra": 0.60, "note": "New production + ventilation shafts"},
        {"year": "FY29", "extra": 0.40, "note": "Full ramp-up"},
        {"year": "FY32", "extra": 0.35, "note": "Additional development"},
    ],
    "Ukwa (Madhya Pradesh)": [
        {"year": "FY27", "extra": 0.35, "note": "Second vertical shaft"},
        {"year": "FY29", "extra": 0.25, "note": "Further development"},
        {"year": "FY32", "extra": 0.20, "note": "Long-term potential"},
    ],
    "Chikla (Maharashtra)": [
        {"year": "FY27", "extra": 0.30, "note": "Second vertical shaft"},
        {"year": "FY29", "extra": 0.35, "note": "Third vertical shaft"},
        {"year": "FY33", "extra": 0.25, "note": "Continued expansion"},
    ],
    "Kandri (Maharashtra)": [
        {"year": "FY28", "extra": 0.40, "note": "New vertical shaft"},
        {"year": "FY31", "extra": 0.25, "note": "Additional capacity"},
    ],
    "Gumgaon (Maharashtra)": [
        {"year": "FY27", "extra": 0.30, "note": "High-speed shaft"},
        {"year": "FY31", "extra": 0.20, "note": "Further development"},
    ],
    "Munsar (Maharashtra)": [
        {"year": "FY27", "extra": 0.20, "note": "Second vertical shaft"},
        {"year": "FY32", "extra": 0.15, "note": "Long-term"},
    ],
}

MAX_MULTIPLIER = {
    "Balaghat (Madhya Pradesh)": 2.10,
    "Dongri Buzurg (Maharashtra)": 1.95,
    "Ukwa (Madhya Pradesh)": 1.85,
    "Chikla (Maharashtra)": 1.90,
    "Kandri (Maharashtra)": 1.80,
    "Gumgaon (Maharashtra)": 1.85,
    "Munsar (Maharashtra)": 1.70,
    "Tirodi (Madhya Pradesh)": 1.60,
    "Beldongri (Maharashtra)": 1.65,
    "Sitapatore (Madhya Pradesh)": 1.75,
}


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def get_mine_history(mine_name):
    return pd.DataFrame({
        "Year": YEARS,
        "Production": [MINE_SPLIT[y].get(mine_name, 0.0) for y in YEARS]
    })


def calculate_cagr(start, end, periods):
    if start <= 0 or periods <= 0:
        return 0.0
    return (end / start) ** (1 / periods) - 1


def get_capacity_uplift(mine_name, year):
    projects = CAPACITY_PROJECTS.get(mine_name, [])
    uplift = 0.0
    year_order = {y: i for i, y in enumerate(FUTURE_YEARS)}
    target_idx = year_order.get(year, 99)
    for p in projects:
        if year_order.get(p["year"], 99) <= target_idx:
            uplift += p["extra"]
    return uplift


def generate_scenarios(mine_name, history):
    fy25 = history["Production"].iloc[-1]
    cagr_4yr = calculate_cagr(history["Production"].iloc[1], fy25, 3)

    rates = {
        "Conservative": max(cagr_4yr * 0.35, 0.004),
        "Base":         max(cagr_4yr * 0.70, 0.012),
        "Optimistic":   max(cagr_4yr * 1.05, 0.025),
    }

    max_cap = fy25 * MAX_MULTIPLIER.get(mine_name, 1.70)
    results = {}

    for name, rate in rates.items():
        preds = []
        current = fy25
        for yr in FUTURE_YEARS:
            current *= (1 + rate)
            uplift = get_capacity_uplift(mine_name, yr)
            realization = 0.75 if yr <= "FY30" else 0.55
            projected = min(current + uplift * realization, max_cap)
            preds.append(round(max(projected, 0.05), 2))
        results[name] = preds

    return results, cagr_4yr, max_cap


def company_impact(mine_name, forecast):
    last = MINE_SPLIT["FY25"][mine_name]
    others = TOTALS["FY25"] - last
    rows = []
    for i, yr in enumerate(FUTURE_YEARS):
        total = others + forecast[i]
        pct = ((total - TOTALS["FY25"]) / TOTALS["FY25"]) * 100
        rows.append({
            "Year": yr,
            "Mine": forecast[i],
            "Company Total": round(total, 2),
            "Δ vs FY25 (%)": round(pct, 1)
        })
    return rows


# ------------------------------------------------------------------
# CSS
# ------------------------------------------------------------------
def inject_css():
    st.markdown("""
    <style>
    .new-header {
        background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
        padding: 28px 32px;
        border-radius: 20px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 32px rgba(15,32,39,0.35);
    }
    .new-header::before {
        content: "";
        position: absolute;
        top: -40%;
        right: -15%;
        width: 380px;
        height: 380px;
        background: radial-gradient(circle, rgba(13,148,136,0.28) 0%, transparent 70%);
        border-radius: 50%;
    }
    .new-header h1 {
        margin: 0;
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -0.3px;
        position: relative;
    }
    .new-header p {
        margin: 8px 0 0 0;
        font-size: 0.95rem;
        opacity: 0.88;
        position: relative;
    }
    .glass-card {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(226,232,240,0.8);
        border-radius: 18px;
        padding: 20px 16px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        transition: all 0.25s ease;
        height: 100%;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 32px rgba(0,0,0,0.10);
    }
    .glass-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .glass-value {
        font-size: 1.65rem;
        font-weight: 800;
        color: #0f766e;
        margin: 0;
        line-height: 1.1;
    }
    .glass-sub {
        font-size: 0.82rem;
        margin-top: 6px;
        font-weight: 600;
    }
    .timeline-item {
        position: relative;
        padding-left: 28px;
        margin-bottom: 18px;
    }
    .timeline-item::before {
        content: "";
        position: absolute;
        left: 0;
        top: 6px;
        width: 12px;
        height: 12px;
        background: #0d9488;
        border-radius: 50%;
        border: 3px solid #ccfbf1;
    }
    .timeline-item::after {
        content: "";
        position: absolute;
        left: 5px;
        top: 20px;
        width: 2px;
        height: calc(100% - 8px);
        background: #e2e8f0;
    }
    .timeline-item:last-child::after {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------------
# Main Page
# ------------------------------------------------------------------
def render():
    inject_css()

    # Header
    st.markdown("""
    <div class="new-header">
        <h1>Production Forecast Engine</h1>
        <p>10-Year Scenario Modelling • Capacity-Adjusted Projections • FY26 – FY35</p>
    </div>
    """, unsafe_allow_html=True)

    # Mine selector
    selected = st.selectbox(
        "Choose Mine",
        options=ALL_MINES,
        index=ALL_MINES.index("Ukwa (Madhya Pradesh)") if "Ukwa (Madhya Pradesh)" in ALL_MINES else 0,
        label_visibility="collapsed"
    )
    st.caption(f"Currently analysing: **{selected}**")

    history = get_mine_history(selected)
    scenarios, hist_cagr, max_cap = generate_scenarios(selected, history)
    fy25 = history["Production"].iloc[-1]
    base_fy35 = scenarios["Base"][-1]
    change = ((base_fy35 - fy25) / fy25) * 100

    # Glass Metric Cards
    st.write("")
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="glass-label">Current (FY25)</div>
            <p class="glass-value">{fy25:.2f}</p>
            <div class="glass-sub" style="color:#64748b;">Lakh MT</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        color = "#059669" if change >= 0 else "#dc2626"
        st.markdown(f"""
        <div class="glass-card">
            <div class="glass-label">Base FY35</div>
            <p class="glass-value">{base_fy35:.2f}</p>
            <div class="glass-sub" style="color:{color};">{change:+.1f}% growth</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="glass-label">4-Yr CAGR</div>
            <p class="glass-value">{hist_cagr*100:.1f}%</p>
            <div class="glass-sub" style="color:#64748b;">FY22 → FY25</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="glass-label">Max Capacity</div>
            <p class="glass-value">{max_cap:.2f}</p>
            <div class="glass-sub" style="color:#64748b;">Ceiling</div>
        </div>
        """, unsafe_allow_html=True)

    # Outlook
    st.write("")
    if change > 15:
        st.success(f"**Strong Growth Trajectory** — Base case indicates **+{change:.1f}%** by FY35")
    elif change > 5:
        st.info(f"**Moderate Growth** — Base case indicates **+{change:.1f}%** by FY35")
    elif change > -5:
        st.warning("**Relatively Stable** — Limited net change expected over 10 years")
    else:
        st.error(f"**Downside Risk** — Base case shows **{change:.1f}%** by FY35")

    # ===================== MAIN FORECAST CHART =====================
    st.markdown("### Forecast Trajectory")

    fig = go.Figure()

    # Historical with area fill
    fig.add_trace(go.Scatter(
        x=history["Year"],
        y=history["Production"],
        mode="lines+markers",
        name="Historical",
        line=dict(color="#0f766e", width=4.5, shape="spline"),
        marker=dict(size=11, color="#0f766e", line=dict(width=2, color="white")),
        fill="tozeroy",
        fillcolor="rgba(15,118,110,0.13)"
    ))

    # Scenarios
    styles = {
        "Conservative": dict(color="#ef4444", dash="dot", width=3),
        "Base":         dict(color="#3b82f6", dash="solid", width=3.5),
        "Optimistic":   dict(color="#10b981", dash="dash", width=3)
    }

    for name, vals in scenarios.items():
        s = styles[name]
        fig.add_trace(go.Scatter(
            x=FUTURE_YEARS,
            y=vals,
            mode="lines+markers",
            name=name,
            line=dict(color=s["color"], width=s["width"], dash=s["dash"], shape="spline"),
            marker=dict(size=8, color=s["color"], line=dict(width=1.5, color="white"))
        ))

    # Fixed vline using index (prevents the TypeError)
    fy30_index = FUTURE_YEARS.index("FY30") if "FY30" in FUTURE_YEARS else 4

    fig.add_vline(
        x=fy30_index,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text="Lower confidence →",
        annotation_position="top",
        annotation_font_size=12,
        annotation_font_color="#64748b"
    )

    fig.update_layout(
        height=500,
        margin=dict(t=40, b=40, l=20, r=20),
        plot_bgcolor="#f8fafc",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="#e2e8f0",
            borderwidth=1
        ),
        yaxis=dict(title="Production (Lakh MT)", gridcolor="#e2e8f0", zeroline=False),
        xaxis=dict(gridcolor="#e2e8f0"),
        hovermode="x unified",
        font=dict(family="Inter, system-ui, sans-serif", size=12)
    )
    st.plotly_chart(fig, use_container_width=True)

    # ===================== SCENARIO TABLE =====================
    st.markdown("### Scenario Breakdown")

    df = pd.DataFrame({
        "Year": FUTURE_YEARS,
        "Conservative": scenarios["Conservative"],
        "Base": scenarios["Base"],
        "Optimistic": scenarios["Optimistic"]
    })

    st.dataframe(
        df.style.format({
            "Conservative": "{:.2f}",
            "Base": "{:.2f}",
            "Optimistic": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    # ===================== CAPACITY TIMELINE =====================
    st.markdown("### Capacity Expansion Timeline")

    projects = CAPACITY_PROJECTS.get(selected, [])
    if projects:
        for p in projects:
            st.markdown(f"""
            <div class="timeline-item">
                <div style="font-weight:700;color:#0f766e;">{p['year']} &nbsp;→&nbsp; +{p['extra']} Lakh MT</div>
                <div style="font-size:0.88rem;color:#64748b;">{p['note']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No major capacity projects currently mapped for this mine.")

    # ===================== COMPANY IMPACT =====================
    st.markdown("---")
    st.markdown("### Company-Level Impact (Base Case)")
    st.caption("Assumes all other mines remain at FY25 production levels")

    impact = company_impact(selected, scenarios["Base"])
    impact_df = pd.DataFrame(impact)

    left, right = st.columns([1.6, 1])

    with left:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=impact_df["Year"],
            y=impact_df["Company Total"],
            marker=dict(
                color=impact_df["Company Total"],
                colorscale=[[0, "#99f6e4"], [0.5, "#14b8a6"], [1, "#0f766e"]],
                line=dict(width=0)
            ),
            text=impact_df["Company Total"],
            textposition="outside",
            textfont=dict(size=12, color="#0f766e"),
            hovertemplate="<b>%{x}</b><br>Company Total: %{y:.2f} Lakh MT<extra></extra>"
        ))
        fig2.add_hline(
            y=TOTALS["FY25"],
            line_dash="dash",
            line_color="#f43f5e",
            line_width=2,
            annotation_text=f"FY25 Baseline ({TOTALS['FY25']})",
            annotation_position="top left",
            annotation_font=dict(size=12, color="#e11d48")
        )
        fig2.update_layout(
            height=400,
            margin=dict(t=30, b=30, l=10, r=10),
            plot_bgcolor="#f8fafc",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(title="Lakh MT", gridcolor="#e2e8f0"),
            xaxis=dict(gridcolor="#e2e8f0"),
            showlegend=False,
            font=dict(family="Inter, system-ui, sans-serif")
        )
        st.plotly_chart(fig2, use_container_width=True)

    with right:
        st.dataframe(
            impact_df[["Year", "Mine", "Company Total", "Δ vs FY25 (%)"]]
            .style.format({
                "Mine": "{:.2f}",
                "Company Total": "{:.2f}",
                "Δ vs FY25 (%)": "{:+.1f}%"
            }),
            use_container_width=True,
            hide_index=True
        )

        final = impact_df.iloc[-1]["Δ vs FY25 (%)"]
        if final > 4:
            st.success(f"This mine can lift total MOIL output by roughly **+{final:.1f}%** by FY35.")
        elif final < -3:
            st.warning(f"This mine may reduce total output by about **{abs(final):.1f}%** by FY35.")
        else:
            st.info("Limited net impact on overall company production.")

    # ===================== NOTES =====================
    with st.expander("Model Notes & Confidence"):
        st.markdown(f"""
- Growth is driven by historical 4-year CAGR + known shaft projects  
- Realization factor drops after FY30 (long-term uncertainty)  
- Hard ceiling applied at **{MAX_MULTIPLIER.get(selected, 1.70):.2f}×** of FY25 production  

**Confidence**  
FY26–28 → Medium-High | FY29–30 → Medium | FY31–35 → Low (directional only)
        """)