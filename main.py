import streamlit as st
import os
import requests
import json
from dotenv import load_dotenv

# Load local .env keys if testing on localhost
load_dotenv()

# =====================================================================
# 1. PAGE SETUP & HIGH-TECH TERMINAL STYLE
# =====================================================================
st.set_page_config(
    page_title="Apex Engine // Terminal",
    page_icon="⚡",
    layout="wide"
)

# Dark Terminal Interface
st.markdown("""
<style>
    .stApp {
        background-color: #0d0f12;
        color: #e2e8f0;
        font-family: 'Courier New', Courier, monospace;
    }
    .stTextArea textarea, .stTextInput input {
        background-color: #1a1f26 !important;
        color: #00ff66 !important;
        border: 1px solid #334155 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. DYNAMIC MULTI-KEY POOL MANAGER
# =====================================================================
def get_api_key_pool():
    """Extracts multiple keys if structured as comma-separated or numbered format."""
    # First check for the continuous comma string
    raw_keys = st.secrets.get("OPENROUTER_API_KEYS", os.getenv("OPENROUTER_API_KEYS", ""))
    if raw_keys:
        return [k.strip() for k in raw_keys.split(",") if k.strip()]
        
    # Check fallback for numbered keys (OPENROUTER_KEY_1, etc.)
    pool = []
    counter = 1
    while True:
        key = st.secrets.get(f"OPENROUTER_KEY_{counter}", os.getenv(f"OPENROUTER_KEY_{counter}", ""))
        if not key:
            break
        pool.append(key.strip())
        counter += 1
        
    return pool

API_POOL = get_api_key_pool()

if "key_index" not in st.session_state:
    st.session_state.key_index = 0

def get_current_key():
    if not API_POOL:
        return None
    return API_POOL[st.session_state.key_index]

def shift_to_next_key():
    if len(API_POOL) <= 1:
        return False
    st.session_state.key_index = (st.session_state.key_index + 1) % len(API_POOL)
    return True

# =====================================================================
# 3. 100% FREE MODEL TIERS
# =====================================================================
MODEL_MAPPING = {
    "⚡ Apex Lite (Fastest Execution)": "meta-llama/llama-3.2-3b-instruct:free",
    "🧠 Apex Logic (Deep Reflection)": "tencent/hy3:free",
    "👑 Apex Pro (Master Logic & Complex Code)": "meta-llama/llama-3.3-70b-instruct:free"
}

# =====================================================================
# 4. CHAT PIPELINE WITH AUTO-FAILOVER
# =====================================================================
def query_apex_engine(messages, selected_model_string):
    model_endpoint = MODEL_MAPPING[selected_model_string]
    attempts = 0
    max_attempts = max(len(API_POOL), 1)
    
    while attempts < max_attempts:
        active_key = get_current_key()
        if not active_key:
            return "❌ [CRITICAL SYSTEM ERROR]: No valid keys detected in your configuration files."
            
        headers = {
            "Authorization": f"Bearer {active_key}",
            "HTTP-Referer": "https://localhost:8501",
            "X-Title": "Apex AI Multi-Tier Terminal",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_endpoint,
            "messages": messages
        }
        
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            if response.status_code == 429:
                st.warning(f"🔄 Line Slot {st.session_state.key_index + 1} rate-limited. Moving to next line...")
                if shift_to_next_key():
                    attempts += 1
                    continue
                else:
                    return "❌ [RATE LIMIT EXHAUSTED]: All free slots are currently resting. Try again in 60s."
                    
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
            
        except Exception as e:
            if shift_to_next_key():
                attempts += 1
                continue
            else:
                return f"❌ [PIPELINE ERROR]: Line failure. Details: {str(e)}"
                
    return "❌ [TIMEOUT]: The server loop could not secure an active endpoint connection."

# =====================================================================
# 5. SIDEBAR CONTROLS & DIAGNOSTICS
# =====================================================================
with st.sidebar:
    st.title("⚡ APEX ENGINE CONFIG")
    st.markdown("---")
    
    # Tier Selection Radio Button
    selected_tier = st.radio("System Execution Depth:", list(MODEL_MAPPING.keys()))
    
    st.markdown("---")
    st.subheader("🌐 Mainframe Diagnostics")
    if API_POOL:
        st.success(f"Signatures Registered: {len(API_POOL)}")
        st.info(f"Active Link Channel: Slot {st.session_state.key_index + 1}")
    else:
        st.error("Zero system signatures detected. Add keys to configuration panel.")

# =====================================================================
# 6. APPLICATION CHAT CORE INTERFACE
# =====================================================================
st.header("⚡ APEX MULTI-TIER NETWORK TERMINAL")

if "history" not in st.session_state:
    st.session_state.history = [{"role": "assistant", "content": "⚡ APEX INTERFACE ONLINE // Multi-key failover protocol active."}]

for msg in st.session_state.history:
    avatar = "🤖" if msg["role"] == "user" else "⚡"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

if user_input := st.chat_input("Pass execution payload..."):
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🤖"):
        st.write(user_input)
        
    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Analyzing data vectors across multi-nodes..."):
            history_payload = [{"role": m["role"], "content": m["content"]} for m in st.session_state.history]
            output = query_apex_engine(history_payload, selected_tier)
            st.write(output)
            
    st.session_state.history.append({"role": "assistant", "content": output})
