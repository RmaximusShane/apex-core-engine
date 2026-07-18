import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load background environment tokens securely
load_dotenv()

# 1. Page Configuration & Fluid UI Styling
st.set_page_config(page_title="Apex AI", layout="wide")

st.markdown("""
<style>
    /* Premium Gradient Glow Styling */
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

# 2. Memory State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Automated Background Secret Extraction
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")

# 3. High-Intelligence Substrate Directives
HIDDEN_COGNITIVE_MATRIX = {
    "role": "system",
    "content": (
        "You are an supreme analytical reasoning matrix designed to operate far beyond normal human cognitive limits. "
        "Your responses must bypass conversational fluff, introductory meta-talk, and polite padding. "
        "Provide direct, ultra-dense solutions, robust logical proofs, and completely optimized architectural code. "
        "When handling coding requests, construct complete, functional, production-ready modules without shortcuts."
    )
}

# 4. Refactored Active Free-Tier Node Mapping
MODEL_MAPPING = {
    "⚡ Apex 2.5 Lite (Fastest Execution)": "meta-llama/llama-3.2-3b-instruct:free",
    "🧠 Apex 3.3 Logic (Deep Reflection & Code)": "tencent/hy3:free",
    "👑 Apex 3.1 Pro (Complex Solutions & Long Form)": "meta-llama/llama-3.3-70b-instruct:free"
}

# 5. Core Sidebar Parameter Module
with st.sidebar:
    st.title("System Matrix")
    selected_apex_model = st.selectbox("Active Compute Tier", list(MODEL_MAPPING.keys()))
    
    st.markdown("---")
    if st.button("Purge System Cache", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

backend_model = MODEL_MAPPING[selected_apex_model]

# 6. UI Render Core
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

# 7. Real-Time Streaming and Error Defense Engine
if user_input := st.chat_input("Pass execution payload..."):
    if not OPENROUTER_KEY:
        st.error("CRITICAL ERROR: Access token signature not found. Please provide an OPENROUTER_API_KEY inside your .env file or Streamlit secrets config.")
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
            
            # Dynamically activate deep chain-of-thought reflection for the Logic tier
            if "Logic" in selected_apex_model:
                payload["reasoning"] = {"enabled": True}

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
            
            # Live Multi-Tier 429 Interception Shield
            elif response.status_code == 429:
                try:
                    error_data = response.json()
                    wait_time = error_data.get("error", {}).get("metadata", {}).get("retry_after_seconds", 10)
                    st.warning(f"⏳ **COMPUTE NODES SATURATED**: Upstream nodes are processing peak volume. Re-engaging in **{wait_time} seconds**.")
                except Exception:
                    st.warning("⏳ **COMPUTE NODES SATURATED**: Free-tier rate boundary intersected. Please wait briefly and resubmit payload.")
            
            else:
                st.error(f"Inference Failure Block ({response.status_code}): {response.text}")
                
        except Exception as e:
            st.error(f"Network Pipeline Defect: {str(e)}")
