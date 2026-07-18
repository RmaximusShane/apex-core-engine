import os
import sys
import json
import time
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class ApexCoreEngine:
    def __init__(self):
        # Fallback to streamlit secrets if running in the cloud, otherwise use .env
        self.api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")
        if not self.api_key:
            st.error("🚨 [CRITICAL ERROR]: OPENROUTER_API_KEY is missing from workspace environment.")
            st.stop()
            
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://apex-core-x.streamlit.app",
            "X-Title": "APEX-CORE-X Reflection Engine"
        })
        
        self.system_manifesto = (
            "IDENTITY: APEX-CORE-X Central Logic Substrate.\n\n"
            "CRITICAL OPERATING MANIFESTO:\n"
            "1. Observe immutable physical, mathematical, and logical axioms natively.\n"
            "2. Prioritize absolute structural correctness over conversational fluff.\n"
            "3. ELIMINATE all pleasantries, introductory summaries, or robotic conclusions.\n"
            "4. METACOGNITION PROTOCOL: You must verify your calculations internally. "
            "If an output violates the user's explicit rules, you are expected to catch it and correct it."
        )

    def _request_silent(self, payload: dict) -> str:
        try:
            response = self.session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                timeout=25
            )
            if response.status_code == 200:
                res_json = response.json()
                return res_json['choices'][0]['message'].get('content', '').strip()
            return f"🚨 [SUBSTRATE ERROR]: Status {response.status_code}"
        except Exception as e:
            return f"🚨 [CONNECTION ERROR]: {str(e)}"

    def execute_logic_silent(self, user_prompt: str, active_model: str, conversation_history: list) -> str:
        # Build memory frame context from the active session history
        memory_buffer = []
        for msg in conversation_history:
            memory_buffer.append({"role": msg["role"], "content": msg["content"]})
            
        if len(memory_buffer) > 10:
            memory_buffer = memory_buffer[-10:]

        # --- PASS 1: GENERATE SILENT DRAFT ---
        draft_payload = {
            "model": active_model, 
            "messages": [{"role": "system", "content": self.system_manifesto}] + memory_buffer,
            "temperature": 0.3,
            "stream": False
        }
        
        draft_response = self._request_silent(draft_payload)
        
        # --- PASS 2: SILENT SELF-CRITIQUE (METACOGNITION) ---
        critique_prompt = (
            f"CRITICAL REVIEW MODE:\n"
            f"Review your draft response above carefully.\n"
            f"Ask yourself: Does this completely fulfill the user's constraints? Are there any logical gaps, "
            f"broken spatial tracks, or code syntax mistakes? \n\n"
            f"If it looks wrong, say: 'Wait, let me check that... actually, that's not right.' and output the clean, fully corrected version.\n"
            f"If it is 100% flawless, simply repeat the output exactly as it is without adding new text."
        )
        
        reflection_messages = [
            {"role": "system", "content": self.system_manifesto},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": draft_response},
            {"role": "user", "content": critique_prompt}
        ]
        
        reflection_payload = {
            "model": active_model,
            "messages": reflection_messages,
            "temperature": 0.1, 
            "stream": False
        }
        
        final_response = self._request_silent(reflection_payload)
        return final_response


# --- STREAMLIT GRAPHICAL USER INTERACTION MATRIX ---
if __name__ == "__main__":
    st.set_page_config(
        page_title="APEX-CORE-X // TERMINAL", 
        page_icon="⚡", 
        layout="wide"
    )

    # 1. PREMIUM HIGH-TECH MOTHERBOARD DARK THEME CSS
    st.markdown(
        """
        <style>
        /* Global Base Override to Charcoal Obsidian */
        .stApp {
            background-color: #04060a !important;
            color: #e2e8f0 !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        
        /* Strict Global Text Bold Enforcer */
        p, span, label, li, h1, h2, h3, textarea, input, button {
            font-weight: bold !important;
        }
        
        /* Motherboard Circuits Welcome Banner */
        .motherboard-welcome {
            border: 2px dashed #00ffcc;
            background: radial-gradient(circle, #091322 0%, #04060a 100%);
            padding: 60px 40px;
            border-radius: 12px;
            box-shadow: 0px 0px 25px rgba(0, 255, 204, 0.15);
            text-align: center;
            margin-top: 12vh;
            margin-bottom: 25px;
        }
        
        .apex-glowing-text {
            font-size: 4rem !important;
            color: #00ffcc !important;
            text-shadow: 0px 0px 15px rgba(0, 255, 204, 0.8), 0px 0px 30px rgba(0, 229, 255, 0.4);
            margin: 0px !important;
            letter-spacing: 5px;
        }
        
        .welcome-subtitle {
            color: #38bdf8 !important;
            font-size: 1.1rem !important;
            letter-spacing: 2px;
            margin-top: 15px !important;
        }

        /* Chat Panel Layout Styles */
        .stChatMessage {
            background-color: #080f1a !important;
            border: 1px solid #112540 !important;
            border-radius: 8px !important;
            padding: 16px !important;
            margin-bottom: 14px !important;
        }
        
        .stChatMessage[data-testid="stChatMessageUser"] {
            border-left: 4px solid #38bdf8 !important;
            background-color: #0b1726 !important;
        }
        
        .stChatInput textarea {
            background-color: #070c14 !important;
            color: #ffffff !important;
            border: 1px solid #00ffcc !important;
        }
        
        .panel-tag {
            color: #00ffcc;
            text-transform: uppercase;
            font-size: 1.2rem;
            margin-bottom: 15px;
            border-bottom: 2px solid #112540;
            padding-bottom: 6px;
            letter-spacing: 2px;
        }

        /* Sidebar Customization */
        section[data-testid="stSidebar"] {
            background-color: #060a12 !important;
            border-right: 1px solid #112540 !important;
        }
        
        /* Sidebar History Log Buttons Override */
        div.element-container button[kind="secondary"] {
            background-color: #091322 !important;
            color: #c9d1d9 !important;
            border: 1px solid #1f3a60 !important;
            text-align: left !important;
            justify-content: flex-start !important;
        }
        div.element-container button[kind="secondary"]:hover {
            border-color: #00ffcc !important;
            color: #00ffcc !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 2. STATE STORAGE INITIALIZATION
    if "engine" not in st.session_state:
        st.session_state.engine = ApexCoreEngine()
        
    # Master tracking matrix for separate session keys
    if "all_sessions" not in st.session_state:
        st.session_state.all_sessions = {}  # Format: { session_timestamp: {"title": str, "messages": list} }
        
    if "active_session_id" not in st.session_state:
        st.session_state.active_session_id = None

    # Premium Free-Tier Backend Processing Endpoints
    MODEL_TIERS = {
        "👑 Apex 3.1 Pro (Frontier Reasoning Tier)": "deepseek/deepseek-r1:free",
        "🚀 Apex 3.1 (High-Capacity Logic Tier)": "meta-llama/llama-3.3-70b-instruct:free",
        "⚡ Apex 2.5 (Fast Efficiency Tier)": "qwen/qwen-2.5-7b-instruct:free"
    }

    # 3. SIDEBAR CONTROL & LOG HISTORY SUBSTRATE
    with st.sidebar:
        st.markdown("### 🎛️ SYSTEM CONTROLS")
        selected_tier = st.selectbox("OPERATIONAL MODEL MATRIX", list(MODEL_TIERS.keys()))
        target_backend_model = MODEL_TIERS[selected_tier]
        
        st.divider()
        
        # --- NEW CHAT CONTROLLER ---
        if st.button("➕ INITIALIZE NEW CHAT", use_container_width=True):
            st.session_state.active_session_id = None
            st.rerun()
            
        st.divider()
        st.markdown("### 🗂️ PREVIOUS LOG RECORDS")
        
        # Render past conversations as selectable high-tech history logs
        if not st.session_state.all_sessions:
            st.write("_No localized log threads detected._")
        else:
            for sess_id in sorted(st.session_state.all_sessions.keys(), reverse=True):
                sess_data = st.session_state.all_sessions[sess_id]
                # Highlight active session visually or label it
                btn_label = f"📟 {sess_data['title']}"
                if st.button(btn_label, key=f"nav_{sess_id}", use_container_width=True):
                    st.session_state.active_session_id = sess_id
                    st.rerun()

    # 4. CHAT LOGIC VIEWPORT FRAMEWORK
    st.markdown('<div class="panel-tag">🧬 APEX COMPUTE CONSOLE LOG</div>', unsafe_allow_html=True)
    
    # Extract the current active sequence arrays
    current_id = st.session_state.active_session_id
    if current_id and current_id in st.session_state.all_sessions:
        active_messages = st.session_state.all_sessions[current_id]["messages"]
    else:
        active_messages = []

    # CONDITIONAL WELCOME SCREEN: Only loads when the viewing terminal array is empty
    if not active_messages:
        st.markdown(
            """
            <div class="motherboard-welcome">
                <p class="apex-glowing-text">APEX CORE</p>
                <p class="welcome-subtitle">SYSTEM OPERATIONAL // ARCHITECTURE STABLE // LOG ENTRY PENDING</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # PERSISTENT DISPLAY FEED
    chat_feed_viewport = st.container()
    with chat_feed_viewport:
        for msg in active_messages:
            with st.chat_message(msg["role"]):
                st.markdown(f"**{msg['content']}**")

    # Command Execution Parsing Point
    if user_prompt := st.chat_input("Inject instruction parameters..."):
        # If no session initialized, construct a fresh storage slot
        if st.session_state.active_session_id is None:
            new_id = str(time.time())
            # Capture first chunk of user prompt to serve as sidebar tab log title
            parsed_title = user_prompt[:22] + "..." if len(user_prompt) > 22 else user_prompt
            st.session_state.all_sessions[new_id] = {
                "title": parsed_title.upper(),
                "messages": []
            }
            st.session_state.active_session_id = new_id
            current_id = new_id
            active_messages = st.session_state.all_sessions[current_id]["messages"]

        # Append user parameter entry row
        active_messages.append({"role": "user", "content": user_prompt})
        with chat_feed_viewport:
            with st.chat_message("user"):
                st.markdown(f"**{user_prompt}**")

            # Route calculation strings directly to backend evaluation loop
            with st.chat_message("assistant"):
                output_placeholder = st.empty()
                with st.spinner("⚡ [ROUTING CIRCUITS VIA INTERNAL METACOGNITIVE LOOP]..."):
                    computed_result = st.session_state.engine.execute_logic_silent(
                        user_prompt, target_backend_model, active_messages
                    )
                output_placeholder.markdown(f"**{computed_result}**")
                
            active_messages.append({"role": "assistant", "content": computed_result})
        
        # Instant refresh coordinates layout nodes perfectly on completion
        st.rerun()
