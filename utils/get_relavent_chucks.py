import numpy as np
#from utils.embedding import embedding_model, index
import streamlit as st

# from sentence_transformers import SentenceTransformer
# import faiss

# embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
# dimension = embedding_model.get_sentence_embedding_dimension()
# index = faiss.IndexFlatL2(dimension)

def get_relevant_chunks(question, all_chunks, all_file_page_mappings, top_k=3):
    try:
        question_embedding = st.session_state.embedding_model.encode(question)
        _, indices = st.session_state.index.search(np.array([question_embedding]), top_k)
        relevant_chunks = [all_chunks[idx] for idx in indices[0]]
        relevant_files_pages = [all_file_page_mappings[idx] for idx in indices[0]]
        return relevant_chunks, relevant_files_pages
    except:
        pass
        #st.error('Error in function --> **get_relevant_chunks**')