import streamlit as st
from rag_engine import BARKEngine
from langchain_core.messages import AIMessage, HumanMessage
import os
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="BARK AI", 
    page_icon="🐾", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Enhanced CSS Styling ---
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Clean background */
    .stApp {
        background: #ffffff;
        padding: 0 1rem;
    }
    
    /* Message styling */
    .message {
        margin: 1.25rem 0;
        display: flex;
        gap: 12px;
    }
    
    .message.user {
        flex-direction: row-reverse;
    }
    
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #f8f9fa;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .message.user .avatar {
        background: #3498db;
        color: white;
    }
    
    .bubble {
        background: #f8f9fa;
        padding: 0.9rem 1.15rem;
        border-radius: 16px;
        max-width: 70%;
        font-size: 0.95rem;
        line-height: 1.5;
        color: #1a202c;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .message.user .bubble {
        background: #3498db;
        color: white;
    }
    
    /* Message animation */
    @keyframes fadeIn {
        from { opacity: 0.8; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message {
        animation: fadeIn 0.2s ease-out;
    }
    
    /* Feedback buttons */
    .feedback {
        margin-left: 52px;
        margin-top: 0.5rem;
        display: flex;
        gap: 8px;
    }
    
    .message.user + .message .feedback {
        display: none;
    }
    
    /* Input styling */
    .stTextInput input {
        border-radius: 25px !important;
        border: 1px solid #d1d5db !important;
        padding: 12px 20px !important;
        font-size: 0.95rem !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    
    .stTextInput input:focus {
        border-color: #3498db !important;
        box-shadow: 0 0 0 2px #ebf4ff !important;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        background: white;
        color: #4a5568;
        font-size: 0.9rem;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
        min-height: 36px;
    }
    
    .stButton button:hover {
        border-color: #3498db;
        color: #3498db;
        background: #f8fafc;
    }
    
    /* Focus states for accessibility */
    button:focus, input:focus {
        outline: 2px solid #3182ce !important;
        outline-offset: 2px !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e0;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a0aec0;
    }
</style>
""", unsafe_allow_html=True)

# --- Engine Loading ---
@st.cache_resource
def load_engine():
    """Load the BARKEngine. This is cached for performance."""
    try:
        return BARKEngine()
    except Exception as e:
        st.error(f"Failed to initialize the BARK Engine: {e}")
        return None

engine = load_engine()
if not engine:
    st.warning("Engine could not be initialized. The app will not function correctly.")
    st.stop()

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm BARK AI. How can I help with your veterinary case today?")
    ]
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# --- Header Section ---
st.markdown("""
<div style='text-align: center; margin-bottom: 1.5rem;'>
    <h1 style='font-size: 2.2rem; margin-bottom: 0.25rem; color: #2c3e50;'>🐾 BARK AI</h1>
    <p style='font-size: 1rem; color: #4a5568; margin-top: 0;'>
        Veterinary Diagnostic Assistant · <span style='font-weight: 500;'>Evidence-Based Answers</span>
    </p>
</div>
""", unsafe_allow_html=True)
st.divider()

# --- Examples Section ---
with st.expander("💡 Example Questions", expanded=True):
    st.caption("Click any example to get started:")
    
    example_prompts = [
        "Older dog with high calcium and non-regenerative anemia - what are the differentials?",
        "Young puppy with acute vomiting - what are common causes?",
        "Dog with frequent urination and litter box straining - diagnostic steps?",
        "Treatment protocol for uncomplicated diabetes in dogs?"
    ]
    
    cols = st.columns(2)
    for i, prompt in enumerate(example_prompts):
        with cols[i % 2]:
            if st.button(
                prompt,
                key=f"ex_{i}",
                use_container_width=True,
                help="Click to use this example"
            ):
                st.session_state.chat_history.append(HumanMessage(content=prompt))
                with st.status("Analyzing veterinary case...", expanded=True) as status:
                    st.write("🔍 Reviewing medical knowledge base")
                    time.sleep(0.5)
                    st.write("📚 Checking latest veterinary guidelines")
                    response = engine.answer(prompt, st.session_state.chat_history)
                    ai_response_content = response.get("answer", "Sorry, I couldn't process that.")
                    status.update(label="Analysis complete", state="complete")
                st.session_state.chat_history.append(AIMessage(content=ai_response_content))
                st.rerun()

# --- Chat History ---
for i, message in enumerate(st.session_state.chat_history):
    is_user = isinstance(message, HumanMessage)
    role = "user" if is_user else "bot"
    avatar = "👩‍⚕️" if is_user else "🐶"
    
    st.markdown(f"""
    <div class="message {role}">
        <div class="avatar">{avatar}</div>
        <div class="bubble">{message.content}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feedback for AI messages (skip for first welcome message)
    if not is_user and i > 0:
        st.markdown('<div class="feedback">', unsafe_allow_html=True)
        col1, col2, _ = st.columns([1, 1, 8])
        
        with col1:
            if st.button("👍 Helpful", key=f"like_{i}"):
                st.session_state.feedback[i] = "like"
                st.toast("Thank you for your feedback!")
                
        with col2:
            if st.button("👎 Needs Improvement", key=f"dislike_{i}"):
                st.session_state.feedback[i] = "dislike"
                st.toast("We'll use this to improve!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- Chat Input ---
if user_query := st.chat_input("Ask about a veterinary case..."):
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.status("Analyzing veterinary case...", expanded=True) as status:
        st.write("🔍 Reviewing medical knowledge base")
        time.sleep(0.5)
        st.write("📚 Checking latest veterinary guidelines")
        response = engine.answer(user_query, st.session_state.chat_history)
        ai_response_content = response.get("answer", "Sorry, I couldn't process that.")
        status.update(label="Analysis complete", state="complete")
    
    st.session_state.chat_history.append(AIMessage(content=ai_response_content))
    st.rerun()
