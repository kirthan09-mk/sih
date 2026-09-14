"""Global CSS and visual styles for the MOIL platform."""
import streamlit as st


def inject_global_css():
    st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1rem;}
    .stMetric, .stMarkdown, .stButton, div[data-testid="stHorizontalBlock"] {
        transition: all 0.3s ease;
    }
    div.st-key-ai_logo button {
        width: 68px !important; height: 68px !important;
        border-radius: 50% !important;
        background: linear-gradient(145deg, #00695c, #00bfa5) !important;
        color: white !important; font-size: 26px !important;
        border: 3px solid white !important;
        box-shadow: 0 8px 25px rgba(0,105,92,0.45) !important;
        position: fixed !important; right: 22px !important; bottom: 22px !important;
        z-index: 999999 !important;
        transition: transform 0.25s ease;
    }
    div.st-key-ai_logo button:hover {
        transform: scale(1.08);
    }
    div.st-key-chat_panel {
        position: fixed !important; right: 22px !important; bottom: 105px !important;
        width: 370px !important; max-height: 520px !important;
        z-index: 999998 !important; background: #ffffff !important;
        border-radius: 14px !important; box-shadow: 0 12px 35px rgba(0,0,0,0.28) !important;
        border: 1px solid #ddd !important; overflow: hidden !important;
        color: #1a1a1a !important;
        animation: fadeIn 0.3s ease;
    }
    div.st-key-chat_panel, div.st-key-chat_panel p, div.st-key-chat_panel div {
        color: #1a1a1a !important;
    }
    div.st-key-chat_panel [data-testid="stChatInput"] textarea {
        color: #1a1a1a !important; background: #fff !important;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)