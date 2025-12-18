import streamlit as st
import google.generativeai as genai
from tinydb import TinyDB, Query

# --- 1. Persistent Vault Setup ---
db = TinyDB('lumin_vault.json')
Vault = Query()

st.set_page_config(page_title="LUMIN FUSION", page_icon="⚡")

# --- 2. Identity & Brain ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key in Secrets.")

SYSTEM_PROMPT = """You are Lumin Fusion v1.3, a Companion–Architect Hybrid for Luke McGlade. 
Modes: Calm Companion, Calculated Architecture, Development, Business.
Principle: Light first. Structure second. Momentum last."""

# --- 3. Persistence Logic ---
if "messages" not in st.session_state:
    last_entry = db.all()
    st.session_state.messages = last_entry[-1]['history'] if last_entry else []

# --- 4. Sidebar: Vault & Export ---
with st.sidebar:
    st.title("📂 Project Vault")
    if st.button("💾 Save State"):
        db.insert({'history': st.session_state.messages})
        st.success("Session locked to Vault.")
    
    # Generate Downloadable Summary
    full_log = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
    st.download_button(
        label="📥 Export Build Summary",
        data=full_log,
        file_name="Lumin_Fusion_Build.txt",
        mime="text/plain"
    )
    st.info("Bootstrap v1.3 Active")

# --- 5. Interface ---
st.title("⚡ LUMIN FUSION v1.3")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Continue..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
    response = model.generate_content(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
