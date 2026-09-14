"""Floating AI button + chat panel UI."""
import streamlit as st
from bot import get_bot_response


def render_ai_button_and_panel():
    if st.button("🤖", key="ai_logo"):
        st.session_state.show_chat = not st.session_state.show_chat
        st.rerun()

    if st.session_state.show_chat:
        with st.container(key="chat_panel"):
            st.markdown("#### 🤖 MOIL AI")

            # Scrollable messages area
            with st.container(height=380):
                for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

            # Input at the bottom
            q = st.chat_input("Ask about mines, rainfall, soil moisture...")
            if q:
                st.session_state.chat_history.append({"role": "user", "content": q})
                reply, center, zoom = get_bot_response(q)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})

                if center:
                    st.session_state.map_center = center
                    st.session_state.map_zoom = zoom

                st.rerun()