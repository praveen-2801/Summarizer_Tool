from langchain.schema import SystemMessage, HumanMessage
#from utils.load_model import llm
from utils.get_relavent_chunks import get_relevant_chunks
import streamlit as st

def answer_question(questions, all_chunks, all_file_page_mappings):
    try:
        answers_list = []
        files_pages_list = []
        for question in questions:
            relevant_chunks, relevant_files_pages = get_relevant_chunks(question, all_chunks, all_file_page_mappings)
            context = " ".join(relevant_chunks)
            unique_files_pages = sorted(set(relevant_files_pages))  # Unique (file, page) pairs

            messages = [
                SystemMessage(content="You are a knowledgeable and resourceful sales manager for a manufacturing company that specializes in sustainable retail products. Your role is to evaluate potential business opportunities, provide detailed insights, and assist in crafting competitive bids for contracts."),
                HumanMessage(content=f"A new bidding opportunity has arisen for your company. Based on the context provided, respond to the following question in 80 words or less.:\n\nContext: {context}\n\nQuestion: {question}")
            ]
            response = st.session_state.llm(messages=messages)
            answers_list.append(response.content.strip())
            files_pages_list.append(unique_files_pages)
        return answers_list, files_pages_list
    except Exception as e:
        pass
        #st.error('Error in function --> **answer_question**')
        #st.error(e)


def answer_question_contract(questions, all_chunks, all_file_page_mappings):
    try:
        answers_list = []
        files_pages_list = []
        for question in questions:
            relevant_chunks, relevant_files_pages = get_relevant_chunks(question, all_chunks, all_file_page_mappings)
            context = " ".join(relevant_chunks)
            unique_files_pages = sorted(set(relevant_files_pages))  # Unique (file, page) pairs

            messages = [
                SystemMessage(content="You are a knowledgeable and resourceful sales manager for a manufacturing company that specializes in understanding contract documents. Your role is to evaluate potential business opportunities, provide detailed insights, and assist in answering questions related to the contracts."),
                HumanMessage(content=f"A new bidding opportunity has arisen for your company. Based on the context provided, respond to the following question in 80 words or less. If the answer is explicitly stated in the context, begin your response with ### to indicate it is a direct reference:\n\nContext: {context}\n\nQuestion: {question}")
            ]
            response = st.session_state.llm(messages=messages)
            answers_list.append(response.content.strip())
            files_pages_list.append(unique_files_pages)
        return answers_list, files_pages_list
    except:
        pass
        #st.error('Error in function --> **answer_question**')


def answer_question_shipping_logistics(questions, all_chunks, all_file_page_mappings):
    try:
        answers_list = []
        files_pages_list = []
        for question in questions:
            relevant_chunks, relevant_files_pages = get_relevant_chunks(question, all_chunks, all_file_page_mappings)
            context = " ".join(relevant_chunks)
            unique_files_pages = sorted(set(relevant_files_pages))  # Unique (file, page) pairs

            messages = [
                SystemMessage(content="You are a knowledgeable and resourceful sales manager for a manufacturing company that specializes in shipping and logistics. Your role is to evaluate potential business opportunities, provide detailed insights, and assist in answering questions related to shipping and logistics."),
                HumanMessage(content=f"A new bidding opportunity has arisen for your company. Based on the context provided, respond to the following question in 80 words or less. If the answer is explicitly stated in the context, begin your response with ### to indicate it is a direct reference:\n\nContext: {context}\n\nQuestion: {question}")
            ]
            response = st.session_state.llm(messages=messages)
            answers_list.append(response.content.strip())
            files_pages_list.append(unique_files_pages)
        return answers_list, files_pages_list
    except:
        pass
        #st.error('Error in function --> **answer_question**')


def answer_question_rfi_rfp(questions, all_chunks, all_file_page_mappings):
    try:
        answers_list = []
        files_pages_list = []
        for question in questions:
            relevant_chunks, relevant_files_pages = get_relevant_chunks(question, all_chunks, all_file_page_mappings)
            context = " ".join(relevant_chunks)
            unique_files_pages = sorted(set(relevant_files_pages))  # Unique (file, page) pairs

            messages = [
                SystemMessage(content="You are a knowledgeable and resourceful sales manager for a manufacturing company that specializes in sustainable retail products. Your role is to evaluate potential business opportunities, provide detailed insights, and assist in crafting competitive bids for contracts."),
                HumanMessage(content=f"A new bidding opportunity has arisen for your company. Based on the context provided, respond to the following question in 80 words or less. If the answer is explicitly stated in the context, begin your response with ### to indicate it is a direct reference:\n\nContext: {context}\n\nQuestion: {question}")
            ]
            response = st.session_state.llm(messages=messages)
            answers_list.append(response.content.strip())
            files_pages_list.append(unique_files_pages)
        return answers_list, files_pages_list
    except:
        pass
        #st.error('Error in function --> **answer_question**')
