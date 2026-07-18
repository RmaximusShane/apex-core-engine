import streamlit as st
import requests
import json

# 1. Page Configuration & Gemini-inspired Glowing CSS
st.set_page_config(page_title="Apex AI", layout="wide")

st.markdown("""
<style>
    /* Premium Glowing Text Style */
    .apex-glow {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(45deg, #FF4B4B, #FF8F00, #4285F4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0;
        filter: drop-shadow(0px 2px 8px rgba(255, 75, 75, 0.3));
    }
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 10vh;
    }
    .subtitle {
        color: #888888;
        text-align: center;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# 2. Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Model Mapping & Selection (Just like Gemini's model switcher)
MODEL_MAPPING = {
    "✨ Apex 2.5 (Fast & Lightweight)": "meta-llama/llama-3.2-3b-instruct:free",
    "🚀 Apex 3.1 (High Intelligence)": "meta-llama/llama-3.3-70b-instruct:free",
    "👑 Apex 3.1 Pro (Frontier Reasoning)": "openrouter/free" # Routes to the single highest-performing active free tier
}

# Sidebar for configuration
with st.sidebar:
    st.title("Settings")
    selected_apex_model = st.selectbox("Select Model Tier", list(MODEL_MAPPING.keys()))
    openrouter_key = st.text_input("OpenRouter API Key", type="password")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Get the true backend model string
backend_model = MODEL_MAPPING[selected_apex_model]

# 4. CONDITIONAL WELCOME SCREEN (Disappears when chat history has items)
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome-container">
            <h1 class="apex-glow">Hello, I'm Apex</h1>
            <p class="subtitle">How can I help you build, create, or think today?</p>
        </div>
    """, unsafe_allow_html=True)

# 5. PERSISTENT CHAT HISTORY RENDER
# Running this outside the input checks guarantees your conversation stays visible!
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. CHAT INPUT AND API ENGINE
if user_input := st.chat_input("Ask Apex anything..."):
    # Immediately append and show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Trigger a rerun right away if it's the first message to clear out the welcome text cleanly
    if len(st.session_state.messages) == 1:
        st.rerun()

    # Call OpenRouter API
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        if not openrouter_key:
            response_placeholder.error("Please add your OpenRouter API Key in the sidebar to begin.")
        else:
            try:
                headers = {
                    "Authorization": f"Bearer {openrouter_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": backend_model,
                    "messages": st.session_state.messages
                }
                
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(payload)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result['choices'][0]['message']['content']
                    response_placeholder.markdown(ai_response)
                    
                    # Save assistant response to history
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    response_placeholder.error(f"API Error ({response.status_code}): {response.text}")
                    
            except Exception as e:
                response_placeholder.error(f"Connection Error: {str(e)}")
