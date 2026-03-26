import streamlit as st
import PyPDF2
import numpy as np
from docx import Document
import pandas as pd


def embed_file(file, file_name):
    try:
        text_chunks = []
        file_page_mapping = []

        file.seek(0)

        if file_name.lower().endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    chunks = [text[i:i + 500] for i in range(0, len(text), 500)]
                    text_chunks.extend(chunks)
                    file_page_mapping.extend([(file_name, page_num + 1)] * len(chunks))

        elif file_name.lower().endswith(".docx"):
            doc = Document(file)
            text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            if text.strip():
                chunks = [text[i:i + 500] for i in range(0, len(text), 500)]
                text_chunks.extend(chunks)
                file_page_mapping.extend([(file_name, 1)] * len(chunks))

        elif file_name.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(file)
            text = df.astype(str).apply(lambda x: " ".join(x), axis=1).str.cat(sep="\n")
            if text.strip():
                chunks = [text[i:i + 500] for i in range(0, len(text), 500)]
                text_chunks.extend(chunks)
                file_page_mapping.extend([(file_name, 1)] * len(chunks))

        if text_chunks:
            embeddings = st.session_state.embedding_model.encode(text_chunks)
            embeddings = np.array(embeddings, dtype="float32")
            st.session_state.index.add(embeddings)

        file.seek(0)
        return text_chunks, file_page_mapping

    except Exception as e:
        st.error(f"Error in embed_file: {str(e)}")
        return [], []
