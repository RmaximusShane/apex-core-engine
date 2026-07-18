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

    def _discover_active_free_model(self) -> str:
        try:
            response = self.session.get("https://openrouter.ai/api/v1/models", timeout=10)
            if response.status_code == 200:
                models_data = response.json().get('data', [])
                free_models = [model['id'] for model in models_data if model['id'].endswith(':free')]
                
                if free_models:
                    preferences = [
                        "meta-llama/llama-3-8b-instruct:free",
                        "qwen/qwen-2.5-7b-instruct:free",
                        "tencent/hy3:free"
                    ]
                    for preferred in preferences:
                        if preferred in free_models:
                            return preferred
                    return free_models[0]
        except Exception:
            pass
            
        return "meta-llama/llama-3-8b-instruct:free"

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

    def execute_logic_silent(self, user_prompt: str) -> str:
        active_model = self._discover_active_free_model()

        # Add user prompt to memory
        self.memory_buffer.append({"role": "user", "content": user_prompt})
        if len(self.memory_buffer) > self.max_memory_turns:
            self.memory_buffer = self.memory_buffer[-self.max_memory_turns:]

        # --- PASS 1: GENERATE SILENT DRAFT ---
        draft_payload = {
            "model": active_model, 
            "messages": [{"role": "system", "content": self.system_manifesto}] + self.memory_buffer,
            "temperature": 0.3,
            "stream": False # Silent background generation
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
            "temperature": 0.1, # Drop temperature down to enforce strict evaluation
            "stream": False # Keep this silent in the background too
        }
        
        final_response = self._request_silent(reflection_payload)
        
        # Commit the finalized response to persistent conversation memory
        self.memory_buffer.append({"role": "assistant", "content": final_response})
        return final_response


# --- STREAMLIT GRAPHICAL USER INTERACTION MATRIX ---
if __name__ == "__main__":
    st.set_page_config(
        page_title="APEX-CORE-X // SUBSTRATE", 
        page_icon="⚡", 
        layout="wide"  # Converted to wide screen to look like a high-tech console layout
    )

    # High-Tech Cyber Motherboard Theme CSS Injection
    st.markdown(
        """
        <style>
        /* Force Deep Cyber Obsidian Background globally */
        .stApp {
            background-color: #05070a !important;
            color: #e2e8f0 !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        
        /* Make body text globally distinct and highly readable */
        p, span, label, li {
            font-weight: 600 !important;
            letter-spacing: 0.5px;
        }

        /* Top Header Board Layout Styling */
        .tech-title-container {
            border: 2px solid #00e5ff;
            background: linear-gradient(90deg, #09121f 0%, #05070a 100%);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 0px 20px rgba(0, 229, 255, 0.25);
            margin-bottom: 25px;
            text-align: center;
        }
        .tech-header {
            color: #00e5ff !important;
            font-size: 2.8rem !important;
            font-weight: 900 !important;
            text-shadow: 0px 0px 12px rgba(0, 229, 255, 0.6);
            margin: 0px !important;
        }
        .tech-subheader {
            color: #38bdf8 !important;
            font-size: 1rem !important;
            font-weight: bold !important;
            letter-spacing: 3px;
            margin-top: 5px !important;
        }

        /* High Tech Gemini Column Custom Grid styling */
        .motherboard-card {
            background-color: #09111c !important;
            border: 1px solid #1e293b !important;
            border-left: 4px solid #00e5ff !important;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.4);
        }

        /* Customize Streamlit built-in chat elements to blend with Gemini Dark theme */
        .stChatMessage {
            background-color: #0b1320 !important;
            border: 1px solid #1e3a8a !important;
            border-radius: 12px !important;
            padding: 16px !important;
            margin-bottom: 15px !important;
            box-shadow: 0px 2px 8px rgba(0, 229, 255, 0.05) !important;
        }
        
        .stChatMessage[data-testid="stChatMessageUser"] {
            border-left: 4px solid #38bdf8 !important;
            background-color: #0d1b2a !important;
        }
        
        /* Input Box Styling Fixes */
        .stChatInput textarea {
            background-color: #09121f !important;
            color: #ffffff !important;
            border: 1px solid #00e5ff !important;
            border-radius: 8px !important;
        }
        
        /* Standardizing bold headers inside blocks */
        .section-tag {
            color: #00e5ff;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 1.1rem;
            margin-bottom: 10px;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Render Main Dashboard Header
    st.markdown(
        """
        <div class="tech-title-container">
            <p class="tech-header">⚡ APEX-CORE-X ENGINE v4.0 ⚡</p>
            <p class="tech-subheader">MULTIMODAL REFLECTION FRAMEWORK // CORE ACTIVE</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Initialize Engine Once within context
    if "engine" not in st.session_state:
        st.session_state.engine = ApexCoreEngine()
        
    # Persistent Web Chat History Setup
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- GEMINI SPLIT LAYOUT SUBSYSTEM ---
    # Column 1 houses the Gemini Core Chat Terminal, Column 2 houses the Multimodal Generation/Editing Array
    chat_col, media_col = st.columns([5, 4], gap="large")

    with chat_col:
        st.markdown('<div class="section-tag">🧬 CENTRAL LOGIC FEED (GEMINI PROTOCOL)</div>', unsafe_allow_html=True)
        
        # Scrolling Chat Substrate Container
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(f"**{msg['content']}**")

        # User Input entry point fixed cleanly below message feed
        if user_input := st.chat_input("Input prompt parameters..."):
            with chat_container:
                # Display current input row
                with st.chat_message("user"):
                    st.markdown(f"**{user_input}**")
                st.session_state.messages.append({"role": "user", "content": user_input})

                # Compute Final output through Metacognition loops
                with st.chat_message("assistant"):
                    status_placeholder = st.empty()
                    with st.spinner("⚡ [ENGAGING MOTHERBOARD CIRCUIT PARALLEL REFLECTION]..."):
                        final_output = st.session_state.engine.execute_logic_silent(user_input)
                    status_placeholder.markdown(f"**{final_output}**")
                    
                st.session_state.messages.append({"role": "assistant", "content": final_output})

    with media_col:
        st.markdown('<div class="section-tag">🎛️ MULTIMODAL GENERATION & EDITING ARRAY</div>', unsafe_allow_html=True)
        
        # --- TAB CONTROLS FOR IMAGE, AUDIO, VIDEO GENERATION/EDITING ---
        img_tab, aud_tab, vid_tab = st.tabs(["🖼️ IMAGE SUBSTRATE", "🎵 AUDIO ENGINE", "🎬 VIDEO PROCESSOR"])
        
        with img_tab:
            st.markdown('<div class="motherboard-card">', unsafe_allow_html=True)
            st.markdown("**IMAGE MANIPULATION & SYNTHESIS UNIT**")
            
            # Setup layout nodes for generation and upload inputs
            img_prompt = st.text_input("🎨 Asset Synthesis Prompt:", placeholder="Describe the image matrix to compile...")
            img_file = st.file_uploader("📥 Source Image Feed (Upload for Editing):", type=["png", "jpg", "jpeg"], key="img_edit")
            
            img_op = st.radio("🛠️ Operation Vector:", ["Compile New Image", "Apply Filter / Edit Matrix", "Deep Structural Scan"], horizontal=True)
            
            if st.button("EXECUTE IMAGE LOGIC ROUTINE", use_container_width=True):
                st.info("⚙️ Image generation/editing pipeline routing active...")
                # Multimodal Hook: Insert image generation API call or PIL matrix manipulation script here
            st.markdown('</div>', unsafe_allow_html=True)
            
        with aud_tab:
            st.markdown('<div class="motherboard-card">', unsafe_allow_html=True)
            st.markdown("**AUDIO SYNTHESIS & WAV SUBSTRATE**")
            
            aud_prompt = st.text_input("🎵 Audio Beat/Vocal Prompt:", placeholder="Specify tempo, genre, or key changes...")
            aud_file = st.file_uploader("📥 Source Audio Track (Upload for Stripping/Editing):", type=["mp3", "wav", "mid"], key="aud_edit")
            
            aud_op = st.selectbox("🛠️ Target Processing Function:", ["Render Instrumental Beat", "Vocal Isolation Splitter", "MIDI Progression Compilation"])
            
            if st.button("EXECUTE AUDIO LOGIC ROUTINE", use_container_width=True):
                st.info("⚙️ Audio sequence parsing initiated...")
                # Multimodal Hook: Connect your FL Studio style file handling or audio generation endpoints here
            st.markdown('</div>', unsafe_allow_html=True)
            
        with vid_tab:
            st.markdown('<div class="motherboard-card">', unsafe_allow_html=True)
            st.markdown("**VIDEO EDITING & KINETIC SYNTHESIS**")
            
            vid_prompt = st.text_input("🎬 Kinetic Video Prompt:", placeholder="Detail camera action, pacing, or sequence specs...")
            vid_file = st.file_uploader("📥 Source Video Feed (Upload for Clipping):", type=["mp4", "mov", "avi"], key="vid_edit")
            
            vid_op = st.select_slider("⚡ Rendering Frame Interpolation Target:", options=["30 FPS Draft", "60 FPS Production", "Cinematic Upscale"])
            
            if st.button("EXECUTE VIDEO LOGIC ROUTINE", use_container_width=True):
                st.info("⚙️ Compiling video render clusters...")
                # Multimodal Hook: Connect custom cinematic generation or video clipping parameters here
            st.markdown('</div>', unsafe_allow_html=True)
