import os
from langchain_openai import ChatOpenAI
import streamlit as st

def load_model():
    """Load ChatOpenAI model (reads key from Streamlit secrets)."""
    # First try Streamlit secrets; fallback to environment
    api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

    if not api_key:
        st.error("❌ OPENAI_API_KEY missing. Please add it in Streamlit → Settings → Secrets.")
        return None

    os.environ["OPENAI_API_KEY"] = api_key

    try:
        if 'llm' not in st.session_state:
            st.session_state.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.2,
                max_tokens=1000
            )
        return st.session_state.llm
    except Exception as e:
        st.error(f"Error initializing ChatOpenAI: {e}")
        return None
