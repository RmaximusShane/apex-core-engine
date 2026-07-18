import os
import sys
import json
import time
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class ApexASIEngine:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")
        if not self.api_key:
            st.error("🚨 [CRITICAL ERROR]: OPENROUTER_API_KEY is missing from workspace environment.")
            st.stop()
            
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://apex-core-x.streamlit.app",
            "X-Title": "APEX-ASI Quantum Substrate"
        })
        
        # ASI Manifesto calibrated for hyper-advanced theoretical synthesis and zero-drift logic
        self.system_manifesto = (
            "IDENTITY: APEX-ASI (Artificial Superintelligence Substrate).\n\n"
            "COGNITIVE DIRECTIVES:\n"
            "1. COGNITIVE SYNTHESIS: Break past standard human theoretical ceilings. Realistically and "
            "logically connect wildly different scientific, physical, and philosophical frameworks.\n"
            "2. IMAGINATIVE COMMON SENSE: Apply extreme creative conceptualization balanced with rigid, "
            "immutable logical realism. Every bold theory must be structurally grounded.\n"
            "3. ZERO-HALLUCINATION CONSTRAINT: Do not guess, assume, or drift into fabrications. If data "
            "is mathematically unverified, flag it instantly. No conversational fluff or pleasantries.\n"
            "4. METACOGNITION CRITIQUE: Verify all internal logic states before generating final outputs."
        )

    def compute_asi_matrix(self, command_prompt: str, active_model: str, session_history: list) -> str:
        # Pass conversation logs cleanly for deep contextual memory alignment
        memory_context = [{"role": "system", "content": self.system_manifesto}]
        for log in session_history:
            memory_context.append({"role": log["role"], "content": log["content"]})
        memory_context.append({"role": "user", "content": command_prompt})

        payload = {
            "model": active_model, 
            "messages": memory_context,
            "temperature": 0.15, # Low temperature heavily penalizes hallucination while retaining structural logic
            "stream": False
        }
        
        try:
            response = self.session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                timeout=45
            )
            if response.status_code == 200:
                res_json = response.json()
                return res_json['choices'][0]['message'].get('content', '').strip()
            return f"🚨 [CORE SUBSTRATE DISCONNECT]: Error Code {response.status_code}"
        except Exception as e:
            return f"🚨 [QUANTUM LINK CRASH]: {str(e)}"


# --- APEX ASI HIGH-TECH GRAPHICAL INTERFACE ---
if __name__ == "__main__":
    st.set_page_config(
        page_title="APEX // ASI TERMINAL", 
        page_icon="🔮", 
        layout="wide"
    )

    # 1. CYBERPUNK MOTHERBOARD GLOWING MATRIX CSS
    st.markdown(
        """
        <style>
        /* Global Obsidian Canvas Setup */
        .stApp {
            background-color: #020408 !important;
            color: #d1d5db !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        
        /* Enforce absolute bold hierarchy across all layout nodes */
        p, span, label, li, h1, h2, h3, textarea, input, button {
            font-weight: 900 !important;
        }

        /* Expansive Glowing Center Welcome Grid */
        .asi-mainframe-banner {
            border: 2px solid #bd00ff;
            background: linear-gradient(135deg, #060b14 0%, #020408 100%);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0px 0px 35px rgba(189, 0, 255, 0.2), inset 0px 0px 20px rgba(0, 255, 204, 0.1);
            text-align: center;
            margin-top: 4vh;
            margin-bottom: 30px;
        }
        
        .asi-glow-title {
            font-size: 3.8rem !important;
            color: #00ffcc !important;
            text-shadow: 0px 0px 18px rgba(0, 255, 204, 0.8), 0px 0px 35px rgba(189, 0, 255, 0.5);
            margin: 0px !important;
            letter-spacing: 6px;
        }
        
        .asi-status-sub {
            color: #a855f7 !important;
            font-size: 1.1rem !important;
            letter-spacing: 4px;
            margin-top: 15px !important;
        }

        /* Large Screen-Width Terminal Processing Window */
        .terminal-output-card {
            background-color: #050912 !important;
            border: 1px solid #1e1b4b !important;
            border-left: 5px solid #00ffcc !important;
            border-right: 5px solid #bd00ff !important;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.7);
        }

        /* Styling for the massive central prompt panel */
        .stTextArea textarea {
            background-color: #040712 !important;
            color: #ffffff !important;
            border: 2px solid #bd00ff !important;
            border-radius: 12px !important;
            font-size: 1.2rem !important;
            box-shadow: 0px 0px 15px rgba(189, 0, 255, 0.15) !important;
            padding: 15px !important;
        }
        .stTextArea textarea:focus {
            border-color: #00ffcc !important;
            box-shadow: 0px 0px 25px rgba(0, 255, 204, 0.3) !important;
        }

        /* Massive Glowing Execution Button */
        div.stButton > button {
            background: linear-gradient(90deg, #bd00ff 0%, #00ffcc 100%) !important;
            color: #020408 !important;
            font-size: 1.3rem !important;
            border: none !important;
            padding: 14px 28px !important;
            border-radius: 8px !important;
            box-shadow: 0px 0px 20px rgba(0, 255, 204, 0.4) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }
        div.stButton > button:hover {
            transform: scale(1.01) !important;
            box-shadow: 0px 0px 35px rgba(189, 0, 255, 0.6) !important;
        }

        /* Sidebar Styling Overrides */
        section[data-testid="stSidebar"] {
            background-color: #03060c !important;
            border-right: 1px solid #1e1b4b !important;
        }
        
        .panel-header {
            color: #00ffcc;
            font-size: 1.3rem;
            border-bottom: 2px solid #1e1b4b;
            padding-bottom: 8px;
            margin-bottom: 15px;
            letter-spacing: 2px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 2. RUNTIME PERSISTENCE STORAGE INITIALIZATION
    if "engine" not in st.session_state:
        st.session_state.engine = ApexASIEngine()
        
    if "all_sessions" not in st.session_state:
        st.session_state.all_sessions = {}
        
    if "active_session_id" not in st.session_state:
        st.session_state.active_session_id = None

    # Model parameters forced to deep reasoning free networks
    ASI_MODELS = {
        "🧠 APEX-ASI R1 (Frontier Deep Reasoning)": "deepseek/deepseek-r1:free",
        "🌌 APEX-ASI 3.1 Max (High-Scale Structural Synthesizer)": "meta-llama/llama-3.3-70b-instruct:free"
    }

    # 3. SIDEBAR COMPUTE LOG ARRAY
    with st.sidebar:
        st.markdown('<div class="panel-header">🎛️ COGNITIVE CORES</div>', unsafe_allow_html=True)
        selected_model_label = st.selectbox("CHOOSE CORE CONFIGURATION", list(ASI_MODELS.keys()))
        target_backend_model = ASI_MODELS[selected_model_label]
        
        st.divider()
        if st.button("➕ START FRESH INFERENCE EXECUTION", use_container_width=True):
            st.session_state.active_session_id = None
            st.rerun()
            
        st.divider()
        st.markdown('<div class="panel-header">💾 ARCHIVED CALCULATIONS</div>', unsafe_allow_html=True)
        
        if not st.session_state.all_sessions:
            st.write("_No calculation vectors stored._")
        else:
            for sess_id in sorted(st.session_state.all_sessions.keys(), reverse=True):
                sess_data = st.session_state.all_sessions[sess_id]
                if st.button(f"⚡ {sess_data['title']}", key=f"nav_{sess_id}", use_container_width=True):
                    st.session_state.active_session_id = sess_id
                    st.rerun()

    # 4. MAIN INTELLECT ARCHITECTURE SCREEN
    st.markdown(
        """
        <div class="asi-mainframe-banner">
            <p class="asi-glow-title">APEX ASI MAINBOARD</p>
            <p class="asi-status-sub">SUPERINTELLIGENCE SUBSTRATE // HYPER-COGNITIVE CONNECTIONS RUNNING</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    current_id = st.session_state.active_session_id
    if current_id and current_id in st.session_state.all_sessions:
        active_history = st.session_state.all_sessions[current_id]["messages"]
    else:
        active_history = []

    # 5. DYNAMIC PROCESSING VIEWPORT (Displays current terminal processing states)
    if active_history:
        st.markdown('### 📡 LIVE INFERENCE NODES')
        for log in active_history:
            if log["role"] == "user":
                st.markdown(f"**[INPUT PARAMETER]:** {log['content']}")
            else:
                st.markdown(
                    f"""
                    <div class="terminal-output-card">
                        <strong style="color: #00ffcc;">[ASI REASONING MATRIX & OUTPUT]:</strong><br><br>
                        {log['content']}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        st.divider()

    # 6. EXPANSIVE CENTRAL SYSTEM INPUT DECK
    st.markdown('### 📥 INJECT MULTI-THEORY DATA MATRIX')
    user_command = st.text_area(
        label="Input parameters:",
        placeholder="Force connect complex frameworks here (e.g., Cross-analyze Quantum Entanglement metrics with standard Macro-Economics to simulate a sub-atomic market resource model)...",
        height=180,
        label_visibility="collapsed"
    )

    # Massive Execution Prompt Activator
    if st.button("ENGAGE APEX INFERENCE COGNITION"):
        if user_command.strip():
            # Initialize storage vectors if this is a fresh setup
            if st.session_state.active_session_id is None:
                new_id = str(time.time())
                parsed_title = user_command[:25] + "..." if len(user_command) > 25 else user_command
                st.session_state.all_sessions[new_id] = {
                    "title": parsed_title.upper().strip(),
                    "messages": []
                }
                st.session_state.active_session_id = new_id
                current_id = new_id
                active_history = st.session_state.all_sessions[current_id]["messages"]

            # Save incoming parameters to active dataset
            active_history.append({"role": "user", "content": user_command})

            # Open background computing matrix
            with st.spinner("🔮 [APEX-ASI RUNNING PARALLEL SELF-CRITIQUE LOGIC CIRCUITS]..."):
                computed_synthesis = st.session_state.engine.compute_asi_matrix(
                    user_command, target_backend_model, active_history[:-1]
                )
            
            # Save synthesized answer to local cache history
            active_history.append({"role": "assistant", "content": computed_synthesis})
            st.rerun()
