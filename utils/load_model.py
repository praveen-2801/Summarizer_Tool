import os
from dotenv import load_dotenv
import streamlit as st

# ✅ Import from the new module (not langchain.chat_models)
from langchain_openai import ChatOpenAI

# Load local .env for local runs (Render ignores it safely)
load_dotenv()

# Safely get the API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "❌ OPENAI_API_KEY not found. Please set it in Render → Environment → Add Environment Variable."
    )

# Ensure the key is available for LangChain
os.environ["OPENAI_API_KEY"] = api_key


def load_model():
    """Load and cache the ChatOpenAI model."""
    try:
        if 'llm' not in st.session_state:
            st.session_state.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.2,
                max_tokens=1000
            )
        return st.session_state.llm
    except Exception as e:
        st.error(f"Error in load_model: {e}")
        return None
