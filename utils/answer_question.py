from langchain.schema import SystemMessage, HumanMessage
from utils.get_relavent_chucks import get_relevant_chunks
import streamlit as st


def _run_questions(questions, all_chunks, all_file_page_mappings, system_prompt, direct_ref=False):
    answers_list = []
    files_pages_list = []

    try:
        if "llm" not in st.session_state or st.session_state.llm is None:
            st.error("LLM is not initialized.")
            return [], []

        if not all_chunks or not all_file_page_mappings:
            st.error("No processed file content found. Please process files first.")
            return [], []

        for question in questions:
            try:
                result = get_relevant_chunks(question, all_chunks, all_file_page_mappings)

                if not result:
                    answers_list.append("No relevant information found.")
                    files_pages_list.append([])
                    continue

                relevant_chunks, relevant_files_pages = result
                context = " ".join(relevant_chunks) if relevant_chunks else ""
                unique_files_pages = sorted(set(relevant_files_pages)) if relevant_files_pages else []

                if not context.strip():
                    answers_list.append("No relevant information found in the uploaded files.")
                    files_pages_list.append(unique_files_pages)
                    continue

                user_prompt = (
                    f"Based only on the context below, answer the question in 80 words or less.\n\n"
                    f"Context:\n{context}\n\n"
                    f"Question:\n{question}"
                )

                if direct_ref:
                    user_prompt += "\n\nIf the answer is explicitly stated in the context, begin your response with ###."

                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt),
                ]

                response = st.session_state.llm.invoke(messages)
                answers_list.append(response.content.strip())
                files_pages_list.append(unique_files_pages)

            except Exception as e:
                st.error(f"Error generating answer for question '{question}': {e}")
                answers_list.append("Error generating answer.")
                files_pages_list.append([])

        return answers_list, files_pages_list

    except Exception as e:
        st.error(f"Error in question answering flow: {e}")
        return [], []


def answer_question(questions, all_chunks, all_file_page_mappings):
    return _run_questions(
        questions,
        all_chunks,
        all_file_page_mappings,
        "You are a knowledgeable and resourceful sales manager for a manufacturing company that specializes in sustainable retail products. Answer strictly from the provided context.",
        direct_ref=False,
    )


def answer_question_contract(questions, all_chunks, all_file_page_mappings):
    return _run_questions(
        questions,
        all_chunks,
        all_file_page_mappings,
        "You are a knowledgeable contract analyst for a manufacturing company. Answer strictly from the provided context.",
        direct_ref=True,
    )


def answer_question_shipping_logistics(questions, all_chunks, all_file_page_mappings):
    return _run_questions(
        questions,
        all_chunks,
        all_file_page_mappings,
        "You are a knowledgeable shipping and logistics analyst for a manufacturing company. Answer strictly from the provided context.",
        direct_ref=True,
    )


def answer_question_rfi_rfp(questions, all_chunks, all_file_page_mappings):
    return _run_questions(
        questions,
        all_chunks,
        all_file_page_mappings,
        "You are a knowledgeable bid and proposal analyst for a manufacturing company. Answer strictly from the provided context.",
        direct_ref=True,
    )
