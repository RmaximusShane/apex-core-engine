import streamlit as st
import requests
import json
import os
import time
from dotenv import load_dotenv

# Load background environment tokens securely
load_dotenv()

# 1. Page Configuration & Fluid UI Styling
st.set_page_config(
    page_title="Apex AI", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom UI Layout Overrides (Responsive Grid + Snowfall Particles + Grok Thinking + Gemini Sidebar & Notebook)
st.markdown("""
<style>
    /* Global Page Background Reset to Crisp Clean White */
    .stApp {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Floating Soft Light-Blue Snowflakes Background Animation */
    .snowflake {
        color: rgba(0, 180, 216, 0.22);
        font-size: 1.2em;
        font-family: Arial, sans-serif;
        text-shadow: 0 0 5px rgba(0, 180, 216, 0.15);
        position: fixed;
        top: -10%;
        z-index: 0;
        user-select: none;
        cursor: default;
        animation: snowflakes-fall 12s linear infinite, snowflakes-shake 4s ease-in-out infinite;
    }

    @keyframes snowflakes-fall {
        0% { top: -10%; }
        100% { top: 100%; }
    }

    @keyframes snowflakes-shake {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(30px); }
    }

    .snowflake:nth-of-type(1) { left: 5%; animation-delay: 0s, 0s; }
    .snowflake:nth-of-type(2) { left: 15%; animation-delay: 2s, 1s; }
    .snowflake:nth-of-type(3) { left: 28%; animation-delay: 4s, 2s; }
    .snowflake:nth-of-type(4) { left: 42%; animation-delay: 1s, 1s; }
    .snowflake:nth-of-type(5) { left: 55%; animation-delay: 6s, 3s; }
    .snowflake:nth-of-type(6) { left: 68%; animation-delay: 3s, 2s; }
    .snowflake:nth-of-type(7) { left: 78%; animation-delay: 7s, 1s; }
    .snowflake:nth-of-type(8) { left: 88%; animation-delay: 5s, 2.5s; }
    .snowflake:nth-of-type(9) { left: 95%; animation-delay: 1.5s, 1.5s; }

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
        transition: all 0.3s ease;
    }
    
    /* Sidebar Input Search Field Styling */
    section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] textarea {
        background-color: #111827 !important;
        color: #f8fafc !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
    }

    /* Ensure text inside dark sidebar remains perfectly legible */
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] span {
        color: #f8fafc !important;
    }

    /* Custom Futuristic Neon Styling for Action Buttons */
    div.stButton > button {
        background: transparent !important;
        color: #00f3ff !important;
        border: 2px solid #00f3ff !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        font-weight: 700 !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.2) !important;
        width: 100% !important;
        font-size: 0.9rem !important;
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

    /* Minimal Clean Chat Interface & Fluid Width Containers */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid #e2e8f0 !important;
        border-radius: 0px !important;
        margin-bottom: 0px !important;
        padding: 20px 12px !important;
        position: relative;
        z-index: 1;
        max-width: 100% !important;
    }
    
    /* Text Typography Adjustments */
    div[data-testid="stChatMessage"] p {
        font-size: 1rem;
        line-height: 1.6;
        color: #0f172a !important;
        font-weight: 500;
        word-break: break-word;
    }

    /* Input Frame Adjustments */
    div[data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 2px solid #0f172a !important;
        border-radius: 8px !important;
        font-weight: 600;
    }

    /* Grok-Style Thinking Block Animation & Styling */
    .grok-thinking-box {
        border-left: 3px solid #00f3ff;
        background-color: #f1f5f9;
        padding: 8px 14px;
        border-radius: 0 8px 8px 0;
        font-family: monospace;
        font-size: 0.88rem;
        color: #475569;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
        width: fit-content;
        max-width: 100%;
    }

    .thinking-spinner {
        width: 10px;
        height: 10px;
        background-color: #00f3ff;
        border-radius: 50%;
        animation: pulseDots 1.2s infinite ease-in-out;
        flex-shrink: 0;
    }

    @keyframes pulseDots {
        0%, 100% { transform: scale(0.6); opacity: 0.4; }
        50% { transform: scale(1.2); opacity: 1; }
    }

    /* Bold Elegant Neon Branding Elements */
    .neon-logo {
        font-size: 2.2rem;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 8px #00f3ff, 0 0 15px #00f3ff;
        font-family: 'Courier New', Courier, monospace;
        margin-right: 10px;
    }
    .brand-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }

    /* High-Impact Neon Text Gradients on Main Screen */
    .apex-glow {
        font-size: clamp(2rem, 6vw, 4rem);
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
        margin-top: 12vh;
        position: relative;
        z-index: 1;
        padding: 0 15px;
    }
    .subtitle {
        color: #475569;
        text-align: center;
        font-size: clamp(0.95rem, 2.5vw, 1.3rem);
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-top: 10px;
    }
    div[data-testid="stSidebarNav"] {display: none;}

    /* ==========================================================================
       RESPONSIVE MEDIA QUERIES FOR ALL SCREEN TYPES (PHONE, TABLET, LAPTOP, TV)
       ========================================================================== */

    /* Mobile Phones (Portrait & Landscape: 320px to 640px) */
    @media screen and (max-width: 640px) {
        .block-container {
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            padding-top: 1rem !important;
        }
        div[data-testid="stChatMessage"] {
            padding: 14px 6px !important;
        }
        div[data-testid="stChatMessage"] p {
            font-size: 0.95rem !important;
        }
        .neon-logo {
            font-size: 1.8rem !important;
        }
        .brand-title {
            font-size: 1.3rem !important;
        }
        div.stButton > button {
            padding: 6px 10px !important;
            font-size: 0.8rem !important;
        }
        .welcome-container {
            margin-top: 6vh !important;
        }
    }

    /* Tablets & Foldables (641px to 1024px) */
    @media screen and (min-width: 641px) and (max-width: 1024px) {
        .block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        div[data-testid="stChatMessage"] p {
            font-size: 1rem !important;
        }
    }

    /* Large Screens & Smart TVs (1920px and above) */
    @media screen and (min-width: 1920px) {
        .block-container {
            max-width: 1400px !important;
            margin: 0 auto !important;
        }
        div[data-testid="stChatMessage"] p {
            font-size: 1.2rem !important;
        }
        .subtitle {
            font-size: 1.6rem !important;
        }
    }
</style>

<!-- Background Ambient Snowflake Layer -->
<div class="snowflake">❄</div>
<div class="snowflake">❅</div>
<div class="snowflake">❆</div>
<div class="snowflake">❄</div>
<div class="snowflake">❅</div>
<div class="snowflake">❆</div>
<div class="snowflake">❄</div>
<div class="snowflake">❅</div>
<div class="snowflake">❆</div>
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
if "notebook_content" not in st.session_state:
    st.session_state.notebook_content = ""

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

# 4. Core Performance Model Mapping (100% Active Free Tiers)
MODEL_MAPPING = {
    "🌐 Apex 2.5 Lite (Fastest Executions and All Round help)": "openrouter/free",
    "🧠 Apex 3.3 Logic (Advanced Reasoning, Core analysis and Analytical Thinking)": "tencent/hy3:free",
    "👑 Apex 3.1 pro Coding Core (Advanced Coding and Agentic Workflow)": "poolside/laguna-m.1:free",
    "⚡ Apex 2.5 Ultra (Extended Thinking)": "nvidia/nemotron-3-ultra-550b-a55b:free",
    "🔮 Open-Weight Reasoning (Apex OSS)": "openrouter/free"
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

# 5. Left Sidebar Deck (Brand Dashboard, Session Search, Gemini Notebook & Memory Control)
with st.sidebar:
    st.markdown('<div style="display: flex; align-items: center; margin-bottom: 20px;"><span class="neon-logo">X</span><span class="brand-title">APEX</span></div>', unsafe_allow_html=True)
    
    if st.button("➕ New Chat", use_container_width=True):
        sync_active_chat_to_history()
        st.session_state.current_chat_id = str(time.time())
        st.session_state.messages = []
        st.session_state.is_processing = False
        st.rerun()
        
    st.markdown("---")
    
    # Gemini-style Sidebar Navigation Tabs (Chats vs Notebook)
    sidebar_tab1, sidebar_tab2 = st.tabs(["💬 Chats", "📓 Notebook"])
    
    with sidebar_tab1:
        # Search Chats Feature
        search_query = st.text_input("🔍 Search Chats", placeholder="Filter signatures...", label_visibility="collapsed")
        
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        
        if not st.session_state.chat_history:
            st.caption("No active sessions cached.")
        else:
            filtered_sessions = {
                cid: cdata for cid, cdata in st.session_state.chat_history.items()
                if search_query.lower() in cdata["title"].lower()
            }
            
            if not filtered_sessions:
                st.caption("No matching signatures found.")
            else:
                for chat_id, chat_data in list(filtered_sessions.items()):
                    is_active = (chat_id == st.session_state.current_chat_id)
                    if st.button(f"⚡ {chat_data['title']}", key=f"session_{chat_id}", use_container_width=True, type="primary" if is_active else "secondary"):
                        sync_active_chat_to_history()
                        st.session_state.current_chat_id = chat_id
                        st.session_state.messages = chat_data["messages"]
                        st.session_state.is_processing = False
                        st.rerun()

    with sidebar_tab2:
        st.caption("Central Scratchpad & Context Builder")
        st.session_state.notebook_content = st.text_area(
            "Scratchpad",
            value=st.session_state.notebook_content,
            height=220,
            placeholder="Type notes, code snippets, or global system rules here...",
            label_visibility="collapsed"
        )
        if st.button("📋 Attach Note to Prompt", use_container_width=True):
            if st.session_state.notebook_content.strip():
                st.session_state.messages.append({
                    "role": "user", 
                    "content": f"[NOTEBOOK CONTEXT]:\n{st.session_state.notebook_content}"
                })
                st.toast("Notebook context attached to chat stream!", icon="📝")
                st.rerun()

    st.markdown(" <div style='margin-top: 6vh;'></div> ", unsafe_allow_html=True)
    st.markdown("---")
    st.caption(f"Signatures Available: Pool [{len(API_KEY_POOL)} keys]")
    
    if st.button("Purge Engine Memory", use_container_width=True):
        st.session_state.chat_history = {}
        st.session_state.current_chat_id = str(time.time())
        st.session_state.messages = []
        st.session_state.key_index = 0
        st.session_state.is_processing = False
        st.session_state.notebook_content = ""
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
            if "thought_duration" in msg and msg["thought_duration"] > 0:
                with st.expander(f"Thought for {msg['thought_duration']} secs", expanded=False):
                    st.caption("Deep analytical reasoning matrix evaluated parameters prior to generating final output payload.")
            st.markdown(msg["content"])

# 7. Real-Time Streaming, Grok Reasoning Container, Key-Rotation, and Self-Healing Engine
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
        # Grok-Style Thinking Live Visual Container
        think_placeholder = st.empty()
        start_time = time.time()
        
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
                # Live dynamic pulse indicator while waiting for first response byte
                elapsed_thinking = int(time.time() - start_time)
                think_placeholder.markdown(
                    f'<div class="grok-thinking-box"><div class="thinking-spinner"></div>Thinking... ({elapsed_thinking}s)</div>', 
                    unsafe_allow_html=True
                )

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

                    # Finalize thinking time computation (Grok Style)
                    final_thinking_time = max(1, int(time.time() - start_time))
                    think_placeholder.empty()
                    
                    with st.expander(f"Thought for {final_thinking_time} secs", expanded=False):
                        st.caption("Deep analytical reasoning matrix evaluated parameters prior to generating final output payload.")

                    full_ai_response = st.write_stream(generate_tokens())
                    
                    # Store assistant message with thinking metadata
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": full_ai_response,
                        "thought_duration": final_thinking_time
                    })
                    
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
                    think_placeholder.empty()
                    status_frame.error(f"Inference Failure Block ({response.status_code}): {response.text}")
                    st.session_state.is_processing = False
                    break
                    
            except Exception as pipeline_error:
                think_placeholder.empty()
                status_frame.error(f"Network Pipeline Defect: {str(pipeline_error)}")
                st.session_state.is_processing = False
                break

        if not stream_processed and keys_attempted >= total_keys:
            think_placeholder.empty()
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
