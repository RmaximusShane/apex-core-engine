import streamlit as st
import requests
import json
import os
import time
from dotenv import load_dotenv

# Load background environment tokens securely
load_dotenv()

# 1. Page Configuration & Fluid UI Styling
st.set_page_config(page_title="Apex AI", layout="wide")

# Custom UI Layout Overrides (Crisp White Base + Radiant Neon Accents & Pulsing Sidebar)
st.markdown("""
<style>
    /* Global Page Background Reset to Crisp Clean White */
    .stApp {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Keyframes for Moving/Pulsing Neon Sidebar Glow */
    @keyframes neonPulse {
        0% {
            box-shadow: 4px 0 15px rgba(0, 243, 255, 0.4), 8px 0 30px rgba(0, 243, 255, 0.2);
            border-right: 2px solid #00f3ff;
        }
        50% {
            box-shadow: 6px 0 25px rgba(255, 0, 255, 0.6), 12px 0 45px rgba(255, 0, 255, 0.3);
            border-right: 2px solid #ff00ff;
        }
        100% {
            box-shadow: 4px 0 15px rgba(0, 243, 255, 0.4), 8px 0 30px rgba(0, 243, 255, 0.2);
            border-right: 2px solid #00f3ff;
        }
    }

    /* Animated Neon Glowing Sidebar Construction */
    section[data-testid="stSidebar"] {
        background-color: #070a13 !important;
        animation: neonPulse 6s infinite ease-in-out;
        transition: all 0.5s ease;
    }
    
    /* Ensure text inside dark sidebar remains perfectly legible */
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] span {
        color: #f8fafc !important;
    }

    /* Custom Futuristic Neon Styling for the New Chat Button Container */
    div.stButton > button {
        background: transparent !important;
        color: #00f3ff !important;
        border: 2px solid #00f3ff !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.2) !important;
        width: 100% !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #00f3ff 0%, #ff00ff 100%) !important;
        color: #ffffff !important;
        border: 2px solid transparent !important;
        box-shadow: 0 0 20px rgba(255, 0, 255, 0.6) !important;
        transform: translateY(-2px) !important;
    }

    div.stButton > button:active {
        transform: scale(0.98) !important;
    }

    /* Minimal Clean Chat Interface */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid #e2e8f0 !important;
        border-radius: 0px !important;
        margin-bottom: 0px !important;
        padding: 24px 16px !important;
    }
    
    /* Elegant Highlight For Text Fields */
    div[data-testid="stChatMessage"] p {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #0f172a !important;
        font-weight: 500;
    }

    /* Input Frame Adjustments */
    div[data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 2px solid #0f172a !important;
        border-radius: 8px !important;
        font-weight: 600;
    }

    /* Bold Elegant Neon Branding Elements */
    .neon-logo {
        font-size: 2.6rem;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 8px #00f3ff, 0 0 15px #00f3ff;
        font-family: 'Courier New', Courier, monospace;
        margin-right: 12px;
    }
    .brand-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }

    /* High-Impact Neon Text Gradients on Main Screen */
    .apex-glow {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00f3ff 0%, #ff00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 10px 0;
        letter-spacing: -1px;
        filter: drop-shadow(0px 4px 12px rgba(0, 243, 255, 0.2));
    }
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 20vh;
    }
    .subtitle {
        color: #475569;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-top: 10px;
    }
    div[data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

# 2. Memory State Engine Check
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(time.time())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "key_index" not in st.session_state:
    st.session_state.key_index = 0 
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# --- MULTI-KEY POOL EXTRACTION ---
keys_raw = os.getenv("OPENROUTER_API_KEYS") or st.secrets.get("OPENROUTER_API_KEYS", "")
if not keys_raw:
    keys_raw = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")

API_KEY_POOL = [k.strip() for k in keys_raw.split(",") if k.strip()]

# 3. High-Intelligence Substrate Directives
HIDDEN_COGNITIVE_MATRIX = {
    "role": "system",
    "content": (
        "You are a supreme analytical reasoning matrix designed to operate far beyond normal human cognitive limits. "
        "Your responses must bypass conversational fluff, introductory meta-talk, and polite padding. "
        "Provide direct, ultra-dense solutions, robust logical proofs, and completely optimized architectural code."
    )
}

# 4. Core Performance Model Mapping (100% Active Free Tiers with Abstract Tech Designators)
MODEL_MAPPING = {
    "🌐 Auto-Shield (Failsafe Free Router)": "openrouter/free",
    "🧠 Deep Logic Substrate (Tencent)": "tencent/hy3:free",
    "👑 Agentic Coding Flagship (Poolside)": "poolside/laguna-m.1:free",
    "⚡ Advanced Reasoning Matrix (Nemotron)": "nvidia/nemotron-3-ultra-550b-a55b:free",
    "🔮 High-Capacity Analytics (Llama 70B)": "meta-llama/llama-3.3-70b-instruct:free"
}

backend_model = MODEL_MAPPING[st.sidebar.selectbox("Active Compute Tier", list(MODEL_MAPPING.keys()), index=0)]

# Background summary generation function for clean titles
def generate_intelligent_title(user_input_text):
    if not API_KEY_POOL:
        return "New Session Matrix"
    
    current_key = API_KEY_POOL[st.session_state.key_index % len(API_KEY_POOL)]
    headers = {
        "Authorization": f"Bearer {current_key}",
        "Content-Type": "application/json"
    }
    
    summary_payload = {
        "model": "openrouter/free", 
        "messages": [
            {"role": "system", "content": "You are a phrase synthesizer. Summarize the user's input into an elegant, clear 2 to 4 word chat title. Do not include quotes, formatting, punctuation, or explanations. Respond with only the summary phrase."},
            {"role": "user", "content": user_input_text}
        ],
        "stream": False
    }
    
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(summary_payload), timeout=5)
        if res.status_code == 200:
            title_text = res.json()["choices"][0]["message"]["content"].strip()
            return title_text if title_text else "New Session Matrix"
    except Exception:
        pass
    
    return user_input_text[:20] + "..." if len(user_input_text) > 20 else user_input_text

def sync_active_chat_to_history():
    if st.session_state.messages:
        if st.session_state.current_chat_id not in st.session_state.chat_history:
            first_user_msg = next((m["content"] for m in st.session_state.messages if m["role"] == "user"), "New Matrix Build")
            derived_title = generate_intelligent_title(first_user_msg)
            st.session_state.chat_history[st.session_state.current_chat_id] = {
                "title": derived_title,
                "messages": st.session_state.messages
            }
        else:
            st.session_state.chat_history[st.session_state.current_chat_id]["messages"] = st.session_state.messages

# 5. Left Sidebar Deck (Brand Dashboard & Session Memory Control)
with st.sidebar:
    st.markdown('<div style="display: flex; align-items: center; margin-bottom: 25px;"><span class="neon-logo">X</span><span class="brand-title">APEX</span></div>', unsafe_allow_html=True)
    
    if st.button("➕ New Session", use_container_width=True):
        sync_active_chat_to_history()
        st.session_state.current_chat_id = str(time.time())
        st.session_state.messages = []
        st.session_state.is_processing = False
        st.rerun()
        
    st.markdown("---")
    st.markdown("### Recent Signatures")
    
    if not st.session_state.chat_history:
        st.caption("No active sessions cached.")
    else:
        for chat_id, chat_data in list(st.session_state.chat_history.items()):
            is_active = (chat_id == st.session_state.current_chat_id)
            if st.button(f"⚡ {chat_data['title']}", key=f"session_{chat_id}", use_container_width=True, type="primary" if is_active else "secondary"):
                sync_active_chat_to_history()
                st.session_state.current_chat_id = chat_id
                st.session_state.messages = chat_data["messages"]
                st.session_state.is_processing = False
                st.rerun()

    st.markdown(" <div style='margin-top: 20vh;'></div> ", unsafe_allow_html=True)
    st.markdown("---")
    st.caption(f"Signatures Available: Pool [{len(API_KEY_POOL)} keys]")
    
    if st.button("Purge Engine Memory", use_container_width=True):
        st.session_state.chat_history = {}
        st.session_state.current_chat_id = str(time.time())
        st.session_state.messages = []
        st.session_state.key_index = 0
        st.session_state.is_processing = False
        st.rerun()

# 6. Main Viewport Render Engine
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome-container">
            <h1 class="apex-glow">APEX COMPUTE CORE</h1>
            <p class="subtitle">Systems configured. Awaiting instructions.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 7. Real-Time Streaming, Key-Rotation, and Self-Healing Engine
input_placeholder = "Input processing instruction payload..." if not st.session_state.is_processing else "Apex is calculating... Please wait."
user_input = st.chat_input(input_placeholder, disabled=st.session_state.is_processing)

if user_input:
    if not API_KEY_POOL:
        st.error("CRITICAL ERROR: No API keys detected in your background environment profile configuration.")
        st.stop()

    st.session_state.is_processing = True
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# Run actual request loop if process lock was triggered
if st.session_state.is_processing and st.session_state.messages:
    last_user_msg = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        payload_messages = [HIDDEN_COGNITIVE_MATRIX] + st.session_state.messages
        
        payload = {
            "model": backend_model,
            "messages": payload_messages,
            "stream": True
        }

        total_keys = len(API_KEY_POOL)
        keys_attempted = 0
        stream_processed = False
        last_wait_time = 12

        status_frame = st.empty()

        while keys_attempted < total_keys and not stream_processed:
            current_key = API_KEY_POOL[st.session_state.key_index % total_keys]
            
            headers = {
                "Authorization": f"Bearer {current_key}",
                "Content-Type": "application/json"
            }
            
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(payload),
                    stream=True
                )
                
                if response.status_code == 200:
                    status_frame.empty()
                    
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
                    stream_processed = True
                    
                    st.session_state.is_processing = False
                    sync_active_chat_to_history()
                    st.rerun()
                
                elif response.status_code == 429:
                    keys_attempted += 1
                    try:
                        error_data = response.json()
                        last_wait_time = int(error_data.get("error", {}).get("metadata", {}).get("retry_after_seconds", 12))
                    except Exception:
                        last_wait_time = 12
                    
                    status_frame.info(f"🔄 Line {st.session_state.key_index % total_keys} saturated. Rotating signatures...")
                    st.session_state.key_index += 1 
                    time.sleep(0.4)
                    
                else:
                    status_frame.error(f"Inference Failure Block ({response.status_code}): {response.text}")
                    st.session_state.is_processing = False
                    break
                    
            except Exception as pipeline_error:
                status_frame.error(f"Network Pipeline Defect: {str(pipeline_error)}")
                st.session_state.is_processing = False
                break

        if not stream_processed and keys_attempted >= total_keys:
            for remaining in range(last_wait_time, 0, -1):
                status_frame.warning(
                    f"🚨 **POOL SATURATION**: All {total_keys} keys hit upstream throttle limits. "
                    f"System cooldown clears in **{remaining}s**..."
                )
                time.sleep(1)
            status_frame.empty()
            st.session_state.is_processing = False
            st.info("🔄 **Pool buffer cycled. Please resubmit your execution payload.**")
            st.rerun()
