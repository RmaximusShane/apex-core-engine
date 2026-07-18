import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables (API Key is hidden in backend)
load_dotenv()

# 1. Page Configuration & Premium Glowing UI Layout
st.set_page_config(page_title="Apex AI", layout="wide")

st.markdown("""
<style>
    /* Premium Glowing Text Style */
    .apex-glow {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(45deg, #FF4B4B, #FF8F00, #4285F4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0;
        filter: drop-shadow(0px 2px 10px rgba(255, 75, 75, 0.3));
    }
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 15vh;
    }
    .subtitle {
        color: #888888;
        text-align: center;
        font-size: 1.25rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# 2. State Engineering Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Fetch Backend API Key Securely
# (Requires a .env file locally containing OPENROUTER_API_KEY=your_key_here)
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")

# 3. Hidden Intelligence Substrate (Zero-Hallucination Cognitive Directives)
HIDDEN_COGNITIVE_MATRIX = {
    "role": "system",
    "content": (
        "You operate as an apex-level cognitive reasoning engine, far surpassing standard human intellect. "
        "Your purpose is pure logical synthesis, solving complex multi-variable problems, and generating flawless architectural code. "
        "Engage in outside-the-box, highly imaginative conceptualization grounded strictly in realistic logic. "
        "Eliminate all fluff, pleasantries, and meta-commentary. Deliver ultra-dense, actionable solutions. "
        "If coding, provide complete, optimized, production-ready scripts."
    )
}

# 4. Strict 3-Tier Execution Framework (Optimized Free Models)
MODEL_MAPPING = {
    "⚡ Apex 2.5 Lite (Fastest Execution)": "meta-llama/llama-3.2-3b-instruct:free",
    "🧠 Apex 3.3 Logic (Deep Reflection & Code)": "deepseek/deepseek-r1:free",
    "👑 Apex 3.1 Pro (Master Logic & Complex Solutions)": "meta-llama/llama-3.3-70b-instruct:free"
}

# 5. Control Deck (Sidebar Configuration)
with st.sidebar:
    st.title("System Parameters")
    selected_apex_model = st.selectbox("Compute Engine Tier", list(MODEL_MAPPING.keys()))
    
    st.markdown("---")
    if st.button("Clear Processing Cache", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

backend_model = MODEL_MAPPING[selected_apex_model]

# 6. Interface Render State Engine
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome-container">
            <h1 class="apex-glow">Hello, I'm Apex</h1>
            <p class="subtitle">How can I help you build, create, or synthesize today?</p>
        </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 7. Real-Time Token Streaming & Error Interception Logic
if user_input := st.chat_input("Input processing instruction..."):
    if not OPENROUTER_KEY:
        st.error("SYSTEM HALTED: Backend API Key is missing. Developer must configure environment variables.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            payload_messages = [HIDDEN_COGNITIVE_MATRIX] + st.session_state.messages
            
            headers = {
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": backend_model,
                "messages": payload_messages,
                "stream": True 
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                stream=True
            )
            
            if response.status_code == 200:
                def generate_tokens():
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode("utf-8").strip()
                            if decoded_line.startswith("data: "):
                                chunk_data = decoded_line[6:]
                                if chunk_data == "[DONE]":
                                    break
                                try:
                                    parsed_json = json.loads(chunk_data)
                                    token = parsed_json["choices"][0]["delta"].get("content", "")
                                    if token:
                                        yield token
                                except Exception:
                                    continue

                full_ai_response = st.write_stream(generate_tokens())
                st.session_state.messages.append({"role": "assistant", "content": full_ai_response})
            
            # --- CUSTOM 429 RATE LIMIT INTERCEPTOR ---
            elif response.status_code == 429:
                error_data = response.json()
                try:
                    # Extract the wait time dynamically from OpenRouter's metadata
                    wait_time = error_data.get("error", {}).get("metadata", {}).get("retry_after_seconds", 10)
                    st.warning(f"⏳ **NETWORK TRAFFIC SATURATED**: The {selected_apex_model} node is temporarily at maximum capacity. Please re-engage in **{wait_time} seconds**.")
                except Exception:
                    st.warning("⏳ **NETWORK TRAFFIC SATURATED**: This free logic node is highly active. Please wait a few seconds and try again.")
            
            else:
                st.error(f"Inference Error ({response.status_code}): {response.text}")
                
        except Exception as e:
            st.error(f"Network Pipeline Breakdown: {str(e)}")
