from sentence_transformers import SentenceTransformer
import faiss
import streamlit as st


def load_embeddings():
    try:
        if "embedding_model" not in st.session_state:
            st.session_state.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        if "dimension" not in st.session_state:
            st.session_state.dimension = st.session_state.embedding_model.get_sentence_embedding_dimension()

        if "index" not in st.session_state:
            st.session_state.index = faiss.IndexFlatL2(st.session_state.dimension)
    except Exception as e:
        st.error(f"Error in load_embeddings: {e}")
