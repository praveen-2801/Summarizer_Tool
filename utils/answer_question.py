from langchain.schema import SystemMessage, HumanMessage
from utils.get_relavent_chucks import get_relevant_chunks
import streamlit as st


def _generate_answers(questions, all_chunks, all_file_page_mappings, system_prompt, direct_ref=False):
    answers_list = []
    files_pages_list = []

    if "llm" not in st.session_state or st.session_state.llm is None:
        st.error("LLM is not initialized. Please check your API key and model setup.")
        return [], []

    if not all_chunks or not all_file_page_mappings:
        st.error("No processed content found. Please upload files and click 'Process Files' first.")
        return [], []

    for question in questions:
        try:
            relevant_chunks, relevant_files_pages = get_relevant_chunks(
                question, all_chunks, all_file_page_mappings
            )

            if not relevant_chunks:
                answers_list.append("No relevant information found in the uploaded files.")
                files_pages_list.append([])
                continue

            context = " ".join(relevant_chunks)
            unique_files_pages = sorted(set(relevant_files_pages))

            human_prompt = (
                f"Based only on the context below, answer the question in 80 words or less.\n\n"
                f"Context:\n{context}\n\n"
                f"Question:\n{question}"
            )

            if direct_ref:
                human_prompt += (
                    "\n\nIf the answer is explicitly stated in the context, start your response with ###."
                )

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]

            response = st.session_state.llm.invoke(messages)
            answers_list.append(response.content.strip())
            files_pages_list.append(unique_files_pages)

        except Exception as e:
            st.error(f"Error generating answer for question '{question}': {e}")
            answers_list.append("Error generating answer.")
            files_pages_list.append([])

    return answers_list, files_pages_list


def answer_question(questions, all_chunks, all_file_page_mappings):
    return _generate_answers(
        questions,
        all_chunks,
        all_file_page_mappings,
        "You are a knowledgeable and resourceful sales manager for a manufacturing company that specializes in sustainable retail products. Answer strictly from the provided context.",
        direct_ref=False
    )


def answer_question_contract(questions, all_chunks, all_file_page_mappings):
    return _generate_answers(
        questions,
        all_chunks,
        all_file_page_mappings,
        "You are a knowledgeable contract analyst for a manufacturing company. Answer strictly from the provided contract context.",
        direct_ref=True
    )


def answer_question_shipping_logistics(questions, all_chunks, all_file_page_mappings):
    return _generate_answers(
        questions,
        all_chunks,
        all_file_page_mappings,
        "You are a knowledgeable shipping and logistics analyst for a manufacturing company. Answer strictly from the provided context.",
        direct_ref=True
    )


def answer_question_rfi_rfp(questions, all_chunks, all_file_page_mappings):
    return _generate_answers(
        questions,
        all_chunks,
        all_file_page_mappings,
        "You are a knowledgeable bid and proposal analyst for a manufacturing company. Answer strictly from the provided context.",
        direct_ref=True
    )
