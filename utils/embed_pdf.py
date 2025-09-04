import streamlit as st
import PyPDF2
import numpy as np
from docx import Document
import pandas as pd

def embed_file(file, file_name):
    try:
        text_chunks = []
        file_page_mapping = []

        # ---------------- PDF ----------------
        if file_name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                chunks = [text[i:i + 500] for i in range(0, len(text), 500)]
                text_chunks.extend(chunks)
                file_page_mapping.extend([(file_name, page_num + 1)] * len(chunks))

        # ---------------- DOCX ----------------
        elif file_name.endswith(".docx"):
            doc = Document(file)
            text = "\n".join([p.text for p in doc.paragraphs])
            chunks = [text[i:i + 500] for i in range(0, len(text), 500)]
            text_chunks.extend(chunks)
            file_page_mapping.extend([(file_name, 1)] * len(chunks))  # no page numbers in docx

        # ---------------- XLSX ----------------
        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(file)
            # Convert entire sheet into text
            text = df.astype(str).apply(lambda x: " ".join(x), axis=1).str.cat(sep="\n")
            chunks = [text[i:i + 500] for i in range(0, len(text), 500)]
            text_chunks.extend(chunks)
            file_page_mapping.extend([(file_name, 1)] * len(chunks))  # treat as single "page"

        # ---------------- Embedding ----------------
        if text_chunks:
            embeddings = [st.session_state.embedding_model.encode(chunk) for chunk in text_chunks]
            st.session_state.index.add(np.array(embeddings))

        return text_chunks, file_page_mapping

    except Exception as e:
        st.error(f'Error in function --> **embed_file**: {str(e)}')
        return [], []
