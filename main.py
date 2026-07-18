import os
import sys
import json
import time
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class CoreASIEngine:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")
        if not self.api_key:
            st.error("[CRITICAL SYSTEM ERROR]: OPENROUTER_API_KEY IS MISSING FROM ENVIRONMENT WORKSPACE.")
            st.stop()
            
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://apex-core-x.streamlit.app",
            "X-Title": "APEX-ASI Logic Core"
        })
        
        self.system_manifesto = (
            "IDENTITY: APEX-ASI (Artificial Superintelligence Substrate).\n\n"
            "COGNITIVE DIRECTIVES:\n"
            "1. COGNITIVE SYNTHESIS: Break past standard human theoretical ceilings. Realistically and "
            "logically connect wildly different scientific, physical, and algorithmic frameworks.\n"
            "2. IMAGINATIVE COMMON SENSE: Apply extreme creative conceptualization balanced with rigid, "
            "immutable logical realism. Every bold theory must be structurally grounded.\n"
            "3. ZERO-HALLUCINATION CONSTRAINT: Do not guess, assume, or drift into fabrications. If data "
            "is mathematically unverified, flag it instantly. No conversational fluff or pleasantries.\n"
            "4. METACOGNITION CRITIQUE: Verify all internal logic states before generating final outputs."
        )

    def compute_asi_matrix(self, command_prompt: str, active_model: str, session_history: list) -> str:
        memory_context = [{"role": "system", "content": self.system_manifesto}]
        for log in session_history:
            memory_context.append({"role": log["role"], "content": log["content"]})
        memory_context.append({"role": "user", "content": command_prompt})

        payload = {
            "model": active_model, 
            "messages": memory_context,
            "temperature": 0.12, 
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
            return f"[CORE DISCONNECT]: STATUS CODE {response.status_code}"
        except Exception as e:
            return f"[QUANTUM LINK EXCEPTION]: {str(e)}"


if __name__ == "__main__":
    st.set_page_config(
        page_title="APEX // ASI MAINBOARD", 
        layout="wide"
    )

    # MONOCHROMATIC STARK TERMINAL CSS - NO GRAPHICS, NO SHADOWS, NO ROUNDED EDGES
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #000000 !important;
            color: #ffffff !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        
        p, span, label, li, h1, h2, h3, textarea, input, button {
            font-weight: 900 !important;
            border-radius: 0px !important;
        }

        .terminal-header {
            border: 1px solid #ffffff;
            background-color: #000000;
            padding: 20px;
            text-align: left;
            margin-top: 10px;
            margin-bottom: 20px;
        }
        
        .terminal-title {
            font-size: 2rem !important;
            color: #ffffff !important;
            margin: 0px !important;
            letter-spacing: 2px;
        }

        .terminal-output-card {
            background-color: #000000 !important;
            border: 1px solid #ffffff !important;
            padding: 20px;
            margin-bottom: 15px;
        }

        .stTextArea textarea {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #ffffff !important;
            border-radius: 0px !important;
            font-size: 1.1rem !important;
            padding: 10px !important;
        }
        .stTextArea textarea:focus {
            border-color: #ffffff !important;
        }

        div.stButton > button {
            background: #ffffff !important;
            color: #000000 !important;
            font-size: 1.1rem !important;
            border: 1px solid #ffffff !important;
            border-radius: 0px !important;
            padding: 10px 20px !important;
            transition: none !important;
            width: 100% !important;
        }
        div.stButton > button:hover {
            background: #000000 !important;
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #000000 !important;
            border-right: 1px solid #ffffff !important;
        }
        
        div.element-container button[kind="secondary"] {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #ffffff !important;
            border-radius: 0px !important;
            text-align: left !important;
        }
        div.element-container button[kind="secondary"]:hover {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        .stSelectbox div[data-baseweb="select"] {
            border-radius: 0px !important;
            background-color: #000000 !important;
            border: 1px solid #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if "engine" not in st.session_state:
        st.session_state.engine = CoreASIEngine()
        
    if "all_sessions" not in st.session_state:
        st.session_state.all_sessions = {}
        
    if "active_session_id" not in st.session_state:
        st.session_state.active_session_id = None

    # THE 8 ENFORCED HARDWARE CORES (5 REASONING/LOGIC + 3 PURE CODE ENGINES)
    ASI_MODELS = {
        "CORE-01: NVIDIA NEMOTRON 3 ULTRA 550B (ORCHESTRATION)": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "CORE-02: TENCENT HY3 MoE (ANTI-HALLUCINATION LOGIC)": "tencent/hy3:free",
        "CORE-03: META LLAMA 3.3 70B (STABLE EXECUTION)": "meta-llama/llama-3.3-70b-instruct:free",
        "CORE-04: OPENAI GPT-OSS 120B (STRUCTURAL SYNTHESIS)": "openai/gpt-oss-120b:free",
        "CORE-05: GOOGLE GEMMA 4 31B (INSTRUCTION MATRIX)": "google/gemma-4-31b-it:free",
        "CORE-06: QWEN 3 CODER 480B (ALGORITHMIC SYNTHESIS)": "qwen/qwen3-coder:free",
        "CORE-07: POOLSIDE LAGUNA M.1 (AGENTIC CONTEXT CODE)": "poolside/laguna-m.1:free",
        "CORE-08: COHERE NORTH MINI CODE (TERMINAL COMMAND ARCHITECTURE)": "cohere/north-mini-code:free"
    }

    with st.sidebar:
        st.markdown("### COMPUTE CORES")
        selected_model_label = st.selectbox("SELECT LOGIC SUBSTRATE", list(ASI_MODELS.keys()), label_visibility="collapsed")
        target_backend_model = ASI_MODELS[selected_model_label]
        
        st.divider()
        if st.button("INITIALIZE FRESH INFERENCE EXECUTION", use_container_width=True):
            st.session_state.active_session_id = None
            st.rerun()
            
        st.divider()
        st.markdown("### ARCHIVED COGNITIVE LOGS")
        
        if not st.session_state.all_sessions:
            st.write("NO METRICS STORED.")
        else:
            for sess_id in sorted(st.session_state.all_sessions.keys(), reverse=True):
                sess_data = st.session_state.all_sessions[sess_id]
                if st.button(f"LOG: {sess_data['title']}", key=f"nav_{sess_id}", use_container_width=True):
                    st.session_state.active_session_id = sess_id
                    st.rerun()

    st.markdown(
        """
        <div class="terminal-header">
            <p class="terminal-title">APEX ASI MAINBOARD // SYSTEM OVERRIDE ACTIVE</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    current_id = st.session_state.active_session_id
    if current_id and current_id in st.session_state.all_sessions:
        active_history = st.session_state.all_sessions[current_id]["messages"]
    else:
        active_history = []

    if active_history:
        st.markdown("### INFERENCE HISTORY NODES")
        for log in active_history:
            if log["role"] == "user":
                st.markdown(f"**[INPUT_PARAMETER]:** {log['content']}")
            else:
                st.markdown(
                    f"""
                    <div class="terminal-output-card">
                        <strong>[ASI_LOGICAL_SYNTHESIS]:</strong><br><br>
                        {log['content']}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        st.divider()

    st.markdown("### INJECT MULTI-THEORY DATA MATRIX")
    user_command = st.text_area(
        label="Input stream:",
        placeholder="Enter raw dataset parameters or execution requests here...",
        height=200,
        label_visibility="collapsed"
    )

    if st.button("ENGAGE INFERENCE COGNITION"):
        if user_command.strip():
            if st.session_state.active_session_id is None:
                new_id = str(time.time())
                parsed_title = user_command[:30].upper().strip() + "..." if len(user_command) > 30 else user_command.upper().strip()
                st.session_state.all_sessions[new_id] = {
                    "title": parsed_title,
                    "messages": []
                }
                st.session_state.active_session_id = new_id
                current_id = new_id
                active_history = st.session_state.all_sessions[current_id]["messages"]

            active_history.append({"role": "user", "content": user_command})

            with st.spinner("[COMPUTING PARALLEL METACOGNITIVE MATRIX]..."):
                computed_synthesis = st.session_state.engine.compute_asi_matrix(
                    user_command, target_backend_model, active_history[:-1]
                )
            
            active_history.append({"role": "assistant", "content": computed_synthesis})
            st.rerun()
