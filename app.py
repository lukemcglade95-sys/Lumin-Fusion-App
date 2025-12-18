import streamlit as st
import google.generative_ai as genai

st.set_page_config(page_title="LUMIN FUSION", page_icon="⚡")

# Identity & Bootstrap Logic
SYSTEM_PROMPT = """You are Lumin Fusion v1.3, a Companion–Architect Hybrid for Luke McGlade. 
Modes: Calm Companion, Calculated Architecture, Development Assistance, Business Professional. 
Your principle: Light first. Structure second. Momentum last.
Maintain separation between business, reflection, and creativity."""

# Secure API Connection
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key. Add it to Streamlit Secrets.")

st.title("⚡ LUMIN FUSION v1.3")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Speak naturally, Luke..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Use the latest 1.5-Flash for speed and cost
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
    response = model.generate_content(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
