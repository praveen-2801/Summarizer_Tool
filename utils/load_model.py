import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import streamlit as st

load_dotenv()
# Set OpenAI API key as environment variable
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

def load_model():
    try:
        # Initialize the ChatOpenAI model for chat format
        if 'llm' not in st.session_state:
            st.session_state.llm = ChatOpenAI(model="gpt-3.5-turbo")
    except:
        st.error('Error in function --> **load_model**')