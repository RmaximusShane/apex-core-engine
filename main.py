import os
import sys
import json
import requests
from dotenv import load_dotenv
import streamlit as st
from PIL import Image

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
        
        self.memory_buffer = []
        self.max_memory_turns = 10  
        
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
        """Handles non-streaming, silent requests to keep reflection backgrounded."""
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

    def execute_logic_silent(self, user_prompt: str, active_model: str) -> str:
        # Synced conversation history mapping
        self.memory_buffer = []
        for msg in st.session_state.messages:
            self.memory_buffer.append({"role": msg["role"], "content": msg["content"]})
            
        if len(self.memory_buffer) > self.max_memory_turns:
            self.memory_buffer = self.memory_buffer[-self.max_memory_turns:]

        # --- PASS 1: GENERATE SILENT DRAFT ---
        draft_payload = {
            "model": active_model, 
            "messages": [{"role": "system", "content": self.system_manifesto}] + self.memory_buffer,
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
        page_title="APEX-CORE-X // MAINBOARD", 
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
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0px 0px 25px rgba(0, 255, 204, 0.15);
            text-align: center;
            margin-top: 8vh;
            margin-bottom: 25px;
        }
        
        .apex-glowing-text {
            font-size: 3.5rem !important;
            color: #00ffcc !important;
            text-shadow: 0px 0px 15px rgba(0, 255, 204, 0.8), 0px 0px 30px rgba(0, 229, 255, 0.4);
            margin: 0px !important;
            letter-spacing: 4px;
        }
        
        .welcome-subtitle {
            color: #38bdf8 !important;
            font-size: 1.1rem !important;
            letter-spacing: 2px;
            margin-top: 15px !important;
        }

        /* Workstation Content Containers */
        .motherboard-card {
            background-color: #080d16 !important;
            border: 1px solid #1e293b !important;
            border-left: 4px solid #00ffcc !important;
            border-radius: 6px;
            padding: 18px;
            margin-bottom: 15px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.5);
        }

        /* Component Panels Layout */
        .stChatMessage {
            background-color: #080f1a !important;
            border: 1px solid #112540 !important;
            border-radius: 8px !important;
            padding: 14px !important;
            margin-bottom: 12px !important;
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
            font-size: 1.1rem;
            margin-bottom: 12px;
            border-bottom: 2px solid #112540;
            padding-bottom: 4px;
            letter-spacing: 1px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 2. INITIALIZE SESSION CORE LOGIC
    if "engine" not in st.session_state:
        st.session_state.engine = ApexCoreEngine()
        
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 3. PREMIUM FREE-TIER FORCED ROUTING MAP
    MODEL_TIERS = {
        "⚡ Apex 2.5 (Fast Efficiency Free Tier)": "qwen/qwen-2.5-7b-instruct:free",
        "🚀 Apex 3.1 (High-Capacity Logic Free Tier)": "meta-llama/llama-3.3-70b-instruct:free",
        "👑 Apex 3.1 Pro (Frontier Reasoning Free Tier)": "deepseek/deepseek-r1:free"
    }

    # Sidebar Control Substrate
    with st.sidebar:
        st.markdown("### 🎛️ SYSTEM CONTROLS")
        selected_tier = st.selectbox("OPERATIONAL MODEL MATRIX", list(MODEL_TIERS.keys()))
        target_backend_model = MODEL_TIERS[selected_tier]
        
        st.divider()
        if st.button("RESET MEMORY BUFFER", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # 4. HORIZONTAL ADVANCED WORKSPACE SPLIT
    chat_col, array_col = st.columns([5, 4], gap="large")

    with chat_col:
        st.markdown('<div class="panel-tag">🧬 APEX LOGIC CONSOLE CORE</div>', unsafe_allow_html=True)
        
        # CONDITIONAL WELCOME GRID: Only renders if no data exists inside the active workspace memory
        if not st.session_state.messages:
            st.markdown(
                """
                <div class="motherboard-welcome">
                    <p class="apex-glowing-text">APEX CORE</p>
                    <p class="welcome-subtitle">SYSTEM OPERATIONAL // ARCHITECTURE STABLE // INPUT PENDING</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        # PERSISTENT CHAT HISTORY RENDER: Positioned outside processing checks to safeguard execution history layout
        chat_feed_viewport = st.container()
        with chat_feed_viewport:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(f"**{msg['content']}**")

        # Command Entry Substrate Loop
        if user_prompt := st.chat_input("Inject instruction parameters..."):
            with chat_feed_viewport:
                with st.chat_message("user"):
                    st.markdown(f"**{user_prompt}**")
                st.session_state.messages.append({"role": "user", "content": user_prompt})

                # Call Dual-Pass Metacognition Core
                with st.chat_message("assistant"):
                    output_placeholder = st.empty()
                    with st.spinner("⚡ [ROUTING CIRCUITS VIA INTERNAL METACOGNITIVE LOOP]..."):
                        computed_result = st.session_state.engine.execute_logic_silent(user_prompt, target_backend_model)
                    output_placeholder.markdown(f"**{computed_result}**")
                    
                st.session_state.messages.append({"role": "assistant", "content": computed_result})
            
            # Instantly rerun context to completely collapse the conditional greeting card on entry
            if len(st.session_state.messages) <= 2:
                st.rerun()

    with array_col:
        st.markdown('<div class="panel-tag">🎚️ MULTIMODAL PRODUCTION ARRAY</div>', unsafe_allow_html=True)
        
        # Workstation Action Interfaces
        img_tab, aud_tab, vid_tab = st.tabs(["🖼️ IMAGE UTILITY", "🎵 AUDIO ENGINE", "🎬 VIDEO ARRAY"])
        
        with img_tab:
            st.markdown('<div class="motherboard-card">', unsafe_allow_html=True)
            st.markdown("**IMAGE EDITING & SYNTHESIS MODULE**")
            img_in = st.text_input("Asset Compile Matrix Prompt:", placeholder="Define visual elements...", key="img_p")
            img_upload = st.file_uploader("Upload Image Source Feed:", type=["png", "jpg", "jpeg"])
            img_action = st.radio("Execution Path:", ["Generate Fresh Visual", "Modify Source Layer Matrix"], horizontal=True)
            if st.button("RUN IMAGE SUBSTRATE ROUTINE", use_container_width=True):
                st.info("Processing target image coordinates...")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with aud_tab:
            st.markdown('<div class="motherboard-card">', unsafe_allow_html=True)
            st.markdown("**AUDIO RENDERING & WAVEFORM SPLITTER**")
            aud_in = st.text_input("Acoustic Spectrum Prompt:", placeholder="Tempo, instrumentation, arrangement specs...", key="aud_p")
            aud_upload = st.file_uploader("Upload Audio Source Feed:", type=["mp3", "wav", "mid"])
            aud_action = st.selectbox("Selected Processing Matrix:", ["Isolate Vocals / Extract Beat", "Compile Algorithmic MIDI Output"])
            if st.button("RUN AUDIO SUBSTRATE ROUTINE", use_container_width=True):
                st.info("Parsing audio data blocks...")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with vid_tab:
            st.markdown('<div class="motherboard-card">', unsafe_allow_html=True)
            st.markdown("**KINETIC VIDEO CLIPPING & SYNTHESIS**")
            vid_in = st.text_input("Kinetic Frame Prompt:", placeholder="Camera movements, lighting style, runtime...", key="vid_p")
            vid_upload = st.file_uploader("Upload Video Source Feed:", type=["mp4", "mov"])
            vid_action = st.select_slider("Target Interpolation Density:", options=["30 FPS Output", "60 FPS Production Master"])
            if st.button("RUN VIDEO SUBSTRATE ROUTINE", use_container_width=True):
                st.info("Compiling frame clusters...")
            st.markdown('</div>', unsafe_allow_html=True)
