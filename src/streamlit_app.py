import streamlit as st
from rag_engine import BARKEngine
from langchain_core.messages import AIMessage, HumanMessage

st.set_page_config(page_title="BARK AI", page_icon="🐾", layout="centered")

st.markdown("""
    <style>
    body {
        background-color: #F9FAFC;
    }
    .stChatMessage {
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 700px;
        word-wrap: break-word;
    }
    .stChatMessage.human {
        background-color: #e8f0fe;
        align-self: flex-end;
        border-left: 4px solid #4285f4;
    }
    .stChatMessage.ai {
        background-color: #ffffff;
        border-left: 4px solid #34a853;
    }
    .stMarkdown p {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stChatInput input {
        font-size: 1rem;
        padding: 12px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🐾 BARK AI")
st.caption("Your AI Co-Pilot for Veterinary Diagnostics")

@st.cache_resource
def load_engine():
    return BARKEngine()

engine = load_engine()
if not engine:
    st.warning("Engine could not be initialized.")
    st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I am BARK AI. How can I assist with your canine case today?")
    ]
if "feedback" not in st.session_state:
    st.session_state.feedback = []

for i, message in enumerate(st.session_state.chat_history):
    role = "AI" if isinstance(message, AIMessage) else "Human"
    with st.chat_message(role, avatar="🐶" if role == "AI" else "🧑‍⚕️"):
        st.markdown(message.content)
        if role == "AI":
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("👍", key=f"like_{i}"):
                    st.session_state.feedback.append(("like", message.content))
            with col2:
                if st.button("👎", key=f"dislike_{i}"):
                    st.session_state.feedback.append(("dislike", message.content))

example_prompt = (
    "An older, lethargic dog presents with a mildly high calcium level (hypercalcemia) "
    "on its blood panel and a non-regenerative anemia. What are the top differential diagnoses to consider?"
)

if user_query := st.chat_input(placeholder=example_prompt):
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("Human", avatar="🧑‍⚕️"):
        st.markdown(user_query)
    with st.chat_message("AI", avatar="🐶"):
        with st.spinner("Analyzing..."):
            response = engine.answer(user_query, st.session_state.chat_history)
            ai_response_content = response["answer"]
            st.markdown(ai_response_content)
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("👍", key="like_final"):
                    st.session_state.feedback.append(("like", ai_response_content))
            with col2:
                if st.button("👎", key="dislike_final"):
                    st.session_state.feedback.append(("dislike", ai_response_content))
    st.session_state.chat_history.append(AIMessage(content=ai_response_content))
    st.rerun()
