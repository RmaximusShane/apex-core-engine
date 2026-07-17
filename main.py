import os
import sys
import json
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
        page_title="APEX-CORE-X", 
        page_icon="⚡", 
        layout="centered"
    )

    # Custom Tech Styling (Web Design UI Elements)
    st.markdown(
        """
        <style>
        /* General background adjustments */
        .stApp {
            background-color: #0d1117;
            color: #c9d1d9;
        }
        /* Custom Header styling */
        .tech-header {
            font-family: 'Courier New', Courier, monospace;
            color: #58a6ff;
            text-align: center;
            font-size: 2.2rem;
            font-weight: bold;
            margin-bottom: 0px;
        }
        .tech-subheader {
            font-family: 'Courier New', Courier, monospace;
            color: #8b949e;
            text-align: center;
            font-size: 0.9rem;
            margin-bottom: 20px;
        }
        /* Style chat inputs and boxes slightly darker */
        .stChatMessage {
            background-color: #161b22 !important;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # UI Header
    st.markdown('<p class="tech-header">⚡ APEX-CORE-X V4 ⚡</p>', unsafe_allow_html=True)
    st.markdown('<p class="tech-subheader">SYSTEM OPERATIONAL // REFLECTION PROTOCOLS ACTIVE</p>', unsafe_allow_html=True)
    st.divider()

    # Initialize Engine Once
    if "engine" not in st.session_state:
        st.session_state.engine = ApexCoreEngine()
        
    # Persistent Web Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Conversation History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User Chat Entry Point
    if user_input := st.chat_input("🧬 System Query..."):
        # Display user question
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Process and deliver polished output
        with st.chat_message("assistant"):
            status_container = st.empty()
            
            # Show a premium high-tech status loading spinner
            with st.spinner("⚡ [COMPUTING CONSTRAINTS & ENGAGING INTERNAL METRIC EVALUATION]..."):
                final_output = st.session_state.engine.execute_logic_silent(user_input)
                
            # Deliver the final polished output instantly 
            status_container.write(final_output)
            
        st.session_state.messages.append({"role": "assistant", "content": final_output})
