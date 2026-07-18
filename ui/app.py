import os
import streamlit as st
import pathlib
import requests
import time
import uuid
import logfire
from dotenv import load_dotenv

# Load environment variables explicitly from the root directory
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=env_path)

# Initialize Logfire
try:
    token = os.getenv("LOGFIRE_TOKEN")
    if not token:
        print("LOGFIRE_TOKEN is empty or None — console tracing only.")
    logfire.configure(token=token)
    LOGFIRE_STATUS = "Connected & Tracing"
except Exception as e:
    print(f"Logfire Init Error in UI: {e}")
    LOGFIRE_STATUS = f"Standby (Error: {e})"

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="QuantumRAG Research Assistant",
    page_icon="🔬",
    layout="wide",
)

# Dark mode toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
with st.sidebar:
    st.session_state.dark_mode = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
css_file = "style.css" if st.session_state.dark_mode else "style_light.css"
css_path = pathlib.Path(__file__).parent / css_file
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)




# --- AVATARS ---
AI_AVATAR = "🔬"
USER_AVATAR = "👤"

# --- SESSION MANAGEMENT ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    logfire.info(f"New User Session Created: {st.session_state.session_id}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>🧠 Research Agent</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Quantum & ML Specialist</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Custom status cards
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; padding: 10px 15px; margin-bottom: 12px;'>
        <div style='font-size: 0.75rem; color: #64748b; font-weight: 600;'>TELEMETRY STATE</div>
        <div style='font-size: 0.9rem; color: #10b981; font-weight: 500; display: flex; align-items: center; gap: 6px;'>
            <span style='height: 8px; width: 8px; background-color: #10b981; border-radius: 50%; display: inline-block;'></span>
            {LOGFIRE_STATUS}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; padding: 10px 15px; margin-bottom: 20px;'>
        <div style='font-size: 0.75rem; color: #64748b; font-weight: 600;'>SESSION ID</div>
        <div style='font-size: 0.9rem; color: #a78bfa; font-weight: 500; font-family: monospace;'>
            {st.session_state.session_id[:16]}...
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ Clear History & Memory", use_container_width=True, type="primary"):
        logfire.warning(f"Memory Wipe Triggered for session: {st.session_state.session_id}")
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

# --- MAIN HEADER ---
st.markdown('<h1 class="main-title">🔬 QuantumRAG</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Research Intelligence Platform for Quantum Computing & Machine Learning</p>', unsafe_allow_html=True)

# --- GREETING & QUICK START LANDING PAGE ---
if not st.session_state.messages:
    st.markdown("""
    <div style='background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; backdrop-filter: blur(10px);'>
        <h3 style='margin-top: 0; font-weight: 600; color: #e2e8f0;'>Welcome to QuantumRAG Assistant</h3>
        <p style='color: #94a3b8; line-height: 1.6;'>
            This advanced agentic pipeline retrieves deep scientific insights and technical documentation specifically in 
            <b>Quantum Computing</b> and <b>Machine Learning</b>. Speak to it naturally to query theoretical models, 
            analyse algorithms, or synthesize findings from recent research papers.
        </p>
        <div style='margin-top: 1.5rem; font-size: 0.85rem; color: #6366F1; font-weight: 600;'>CHOOSE A RESEARCH PROMPT TO START:</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="quickstart-card">', unsafe_allow_html=True)
        if st.button("🌀 Shor's Factoring\n\nExplain Shor's algorithm and its cryptographic implications.", key="qs1", use_container_width=True):
            st.session_state.clicked_prompt = "Explain Shor's algorithm and its implications for RSA encryption."
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="quickstart-card">', unsafe_allow_html=True)
        if st.button("🧠 Variational Circuits\n\nHow do variational quantum classifiers function?", key="qs2", use_container_width=True):
            st.session_state.clicked_prompt = "Describe the training process of a Variational Quantum Classifier (VQC)."
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="quickstart-card">', unsafe_allow_html=True)
        if st.button("⚡ Quantum Advantage\n\nWhat is quantum advantage and how is it verified?", key="qs3", use_container_width=True):
            st.session_state.clicked_prompt = "What is quantum advantage, and what are the current benchmarks used to demonstrate it?"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="quickstart-card">', unsafe_allow_html=True)
        if st.button("📈 Attention Mechanisms\n\nExplain multi-head self-attention in deep learning transformers.", key="qs4", use_container_width=True):
            st.session_state.clicked_prompt = "How do transformers utilize multi-head self-attention mechanisms in deep learning?"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- RENDER CHAT HISTORY ---
for i, message in enumerate(st.session_state.messages):
    role_key = "user" if message["role"] == "user" else "assistant"
    # Wrapping st.chat_message inside a container with unique key enables custom CSS styling per role
    with st.container(key=f"{role_key}_msg_{i}"):
        avatar = AI_AVATAR if message["role"] == "assistant" else USER_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# --- CHAT INTERACTION LOGIC ---
prompt = None

# Check if a card was clicked
if "clicked_prompt" in st.session_state and st.session_state.clicked_prompt:
    prompt = st.session_state.clicked_prompt
    st.session_state.clicked_prompt = None

# Check if new message input was entered
chat_input_val = st.chat_input("Ask about quantum algorithms, ML architectures, recent papers...")
if chat_input_val:
    prompt = chat_input_val

if prompt:
    # Append user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.container(key=f"user_msg_{len(st.session_state.messages)}"):
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

    # Generate assistant response
    with st.container(key=f"assistant_msg_{len(st.session_state.messages)}"):
        with st.chat_message("assistant", avatar=AI_AVATAR):
            with st.status("🔍 Querying QuantumRAG Pipeline...", expanded=True) as status:
                try:
                    # Distributed tracing of API backend call
                    with logfire.span("Calling RAG Backend"):
                        base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
                        url = f"{base_url}/query"
                        payload = {"q": prompt, "thread_id": st.session_state.session_id}
                        response = requests.post(url, json=payload, timeout=60)
                        data = response.json()
                    
                    # Style Reasoning Steps inside terminal console
                    steps = data.get("thought_process", [])
                    if steps:
                        steps_html = "".join([f'<div class="console-line">> {step}</div>' for step in steps])
                        st.markdown(f"""
                        <div class="console-box">
                            <div class="console-header">
                                <span class="console-dot dot-red"></span>
                                <span class="console-dot dot-yellow"></span>
                                <span class="console-dot dot-green"></span>
                                <span class="console-title">agentic_spans.log</span>
                            </div>
                            <div style="max-height: 220px; overflow-y: auto; padding-right: 5px;">
                                {steps_html}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    status.update(label="✅ Research Complete", state="complete", expanded=False)
                    
                    # Style Retrieved Sources as grid cards
                    sources = data.get("sources", [])
                    if sources:
                        with st.expander(f"📄 Retrieved Research Context ({len(sources)} chunks)", expanded=False):
                            cards_html = ""
                            for i, source in enumerate(sources):
                                snippet = source.replace("CONTENT:", "").strip()
                                preview = snippet[:150] + "..." if len(snippet) > 150 else snippet
                                cards_html += f"""
                                <div class="source-card">
                                    <div class="source-title">📄 Chunk {i+1}</div>
                                    <div class="source-snippet">{preview}</div>
                                </div>
                                """
                            st.markdown(f'<div class="source-grid">{cards_html}</div>', unsafe_allow_html=True)
                            
                            st.markdown('<p style="font-size: 0.85rem; color: #64748b; font-weight: 600; margin: 1.5rem 0 0.5rem 0;">FULL CHUNK TEXTS</p>', unsafe_allow_html=True)
                            for i, source in enumerate(sources):
                                snippet = source.replace("CONTENT:", "").strip()
                                st.text_area(f"Chunk {i+1}", snippet, height=120, disabled=True)
                    else:
                        st.caption("ℹ️ No technical context retrieved — conversational response.")
                        
                except Exception as e:
                    logfire.error(f"UI-Backend Connection Failed: {e}")
                    status.update(label="❌ Connection Failed", state="error")
                    st.error("RAG Backend is offline or unreachable.")
                    st.stop()

            # Stream response in word chunks for smoothness and speed
            answer_placeholder = st.empty()
            full_answer = data.get("answer", "I apologize, but I could not synthesize a response.")
            
            words = full_answer.split(" ")
            curr_text = ""
            for i, word in enumerate(words):
                curr_text += word + " "
                answer_placeholder.markdown(curr_text + "▌")
                time.sleep(0.015)
            
            answer_placeholder.markdown(full_answer)
            st.session_state.messages.append({"role": "assistant", "content": full_answer})
            logfire.info("Chat cycle completed successfully.")
            st.rerun()
