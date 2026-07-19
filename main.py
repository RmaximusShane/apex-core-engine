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

# Custom UI Layout Overrides (Sleek Minimal Cybernetic Theme)
st.markdown("""
<style>
    /* Global Page Background & Text Base Override */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0c101b 0%, #05070f 100%) !important;
        color: #e2e8f0 !important;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Sidebar Structural Styling */
    section[data-testid="stSidebar"] {
        background-color: #070911 !important;
        border-right: 1px solid #161f38 !important;
    }

    /* Minimal Stark Chat Messages Box Container Tweaks */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 0px !important;
        margin-bottom: 0px !important;
        padding: 24px 12px !important;
    }
    
    /* Slight tint shift for assistant replies to give clean structure */
    div[data-testid="stChatMessage"][data-testid="stChatMessageContent"] {
        background-color: rgba(255, 255, 255, 0.01) !important;
    }

    /* Input Box Styles */
    div[data-testid="stChatInput"] textarea {
        background-color: #0d1324 !important;
        color: #00f3ff !important;
        border: 1px solid #161f38 !important;
        border-radius: 8px !important;
    }

    /* Top Sidebar Branding Custom Layout Elements */
    .neon-logo {
        font-size: 2.4rem;
        font-weight: 900;
        color: #FFFFFF;
        text-shadow: 0 0 5px #00f3ff, 0 0 10px #00f3ff, 0 0 20px #00f3ff;
        font-family: 'Courier New', Courier, monospace;
        margin-right: 12px;
        user-select: none;
    }
    .brand-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 0.5px;
        font-family: system-ui, -apple-system, sans-serif;
    }

    /* Welcome Main Viewport Header Styles */
    .apex-glow {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #00f3ff, #4285F4, #FF00FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0;
        filter: drop-shadow(0px 2px 8px rgba(0, 243, 255, 0.3));
    }
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 15vh;
    }
    .subtitle {
        color: #64748b;
        text-align: center;
        font-size: 1.25rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    div[data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

# 2. Advanced Multi-Session Memory Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(time.time())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "key_index" not in st.session_state:
    st.session_state.key_index = 0 # Tracks which key in the pool is currently active

def sync_active_chat_to_history():
    if st.session_state.messages:
        if st.session_state.current_chat_id not in st.session_state.chat_history:
            first_user_msg = next((m["content"] for m in st.session_state.messages if m["role"] == "user"), "New Engine Log")
            derived_title = first_user_msg[:24] + "..." if len(first_user_msg) > 24 else first_user_msg
            st.session_state.chat_history[st.session_state.current_chat_id] = {
                "title": derived_title,
                "messages": st.session_state.messages
            }
        else:
            st.session_state.chat_history[st.session_state.current_chat_id]["messages"] = st.session_state.messages

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

# 4. Core Performance Model Mapping (Updated active free models)
MODEL_MAPPING = {
    "⚡ Apex 2.5 Lite (Fast General Text)": "openai/gpt-oss-20b:free",
    "🧠 Apex 3.3 Logic (Deep Frontier Reasoning)": "nvidia/nemotron-3-ultra-550b-a55b:free",
    "👑 Apex 3.1 Pro (Advanced Code & Math)": "qwen/qwen3-coder:free"
}

# 5. Left Sidebar Deck (Brand Dashboard & Session Memory Control)
with st.sidebar:
    st.markdown('<div style="display: flex; align-items: center; margin-bottom: 25px;"><span class="neon-logo">X</span><span class="brand-title">Apex</span></div>', unsafe_allow_html=True)
    
    if st.button("➕ New Chat", use_container_width=True):
        sync_active_chat_to_history()
        st.session_state.current_chat_id = str(time.time())
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("### Recent")
    
    if not st.session_state.chat_history:
        st.caption("No recent processing matrices recorded.")
    else:
        for chat_id, chat_data in list(st.session_state.chat_history.items()):
            is_active = (chat_id == st.session_state.current_chat_id)
            if st.button(f"💬 {chat_data['title']}", key=f"session_{chat_id}", use_container_width=True, type="primary" if is_active else "secondary"):
                sync_active_chat_to_history()
                st.session_state.current_chat_id = chat_id
                st.session_state.messages = chat_data["messages"]
                st.rerun()

    st.markdown(" <div style='margin-top: 25vh;'></div> ", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Matrix Configuration")
    selected_apex_model = st.selectbox("Active Compute Tier", list(MODEL_MAPPING.keys()))
    
    st.caption(f"Loaded Compute Signatures: Pool [{len(API_KEY_POOL)} keys]")
    
    if st.button("Purge System Cache", use_container_width=True):
        st.session_state.chat_history = {}
        st.session_state.current_chat_id = str(time.time())
        st.session_state.messages = []
        st.session_state.key_index = 0
        st.rerun()

backend_model = MODEL_MAPPING[selected_apex_model]

# 6. Main Viewport Render Engine
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

# 7. Real-Time Streaming, Key-Rotation, and Self-Healing Engine
if user_input := st.chat_input("Pass execution payload..."):
    if not API_KEY_POOL:
        st.error("CRITICAL ERROR: No API keys detected in your background .env profile config.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        payload_messages = [HIDDEN_COGNITIVE_MATRIX] + st.session_state.messages
        
        payload = {
            "model": backend_model,
            "messages": payload_messages,
            "stream": True
        }
        
        if "Logic" in selected_apex_model:
            payload["reasoning"] = {"enabled": True}

        total_keys = len(API_KEY_POOL)
        keys_attempted = 0
        stream_processed = False
        global_cooldown_needed = False
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
                    sync_active_chat_to_history()
                
                elif response.status_code == 429:
                    keys_attempted += 1
                    try:
                        error_data = response.json()
                        last_wait_time = int(error_data.get("error", {}).get("metadata", {}).get("retry_after_seconds", 12))
                    except Exception:
                        last_wait_time = 12
                    
                    status_frame.info(f"🔄 Compute Signature Slot {st.session_state.key_index % total_keys} saturated. Switching lines...")
                    st.session_state.key_index += 1 
                    time.sleep(0.4)
                    
                else:
                    status_frame.error(f"Inference Failure Block ({response.status_code}): {response.text}")
                    break
                    
            except Exception as pipeline_error:
                status_frame.error(f"Network Pipeline Defect: {str(pipeline_error)}")
                break

        if not stream_processed and keys_attempted >= total_keys:
            global_cooldown_needed = True
            for remaining in range(last_wait_time, 0, -1):
                status_frame.warning(
                    f"🚨 **ENTIRE COMPUTE POOL SATURATED**: All {total_keys} keys hit upstream limits. "
                    f"Global safety structural freeze clears in **{remaining}s**..."
                )
                time.sleep(1)
            status_frame.empty()
            st.info("🔄 **Pool buffer cycled. Please resubmit your execution payload.**")
