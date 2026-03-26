import numpy as np
import streamlit as st


def get_relevant_chunks(question, all_chunks, all_file_page_mappings, top_k=3):
    try:
        if not all_chunks or not all_file_page_mappings:
            return [], []

        if "index" not in st.session_state or st.session_state.index.ntotal == 0:
            return [], []

        question_embedding = st.session_state.embedding_model.encode(question)
        k = min(top_k, len(all_chunks))

        distances, indices = st.session_state.index.search(
            np.array([question_embedding], dtype="float32"), k
        )

        valid_indices = [idx for idx in indices[0] if 0 <= idx < len(all_chunks)]

        relevant_chunks = [all_chunks[idx] for idx in valid_indices]
        relevant_files_pages = [all_file_page_mappings[idx] for idx in valid_indices]

        return relevant_chunks, relevant_files_pages

    except Exception as e:
        st.error(f"Error in get_relevant_chunks: {e}")
        return [], []
