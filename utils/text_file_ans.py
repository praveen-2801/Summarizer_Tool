from io import StringIO, BytesIO
import streamlit as st

def get_text_file(questions, answers_list, files_pages_list):
    try:
        output = StringIO()
        output.write("PDF QUESTION ANSWERING REPORT\n")
        output.write("="*100 + "\n\n")
        iter = 1
        for question in questions:
            # Apply formatting by capitalizing and surrounding with symbols
            output.write(f"#### QUESTION {iter}: {question.upper()} ####\n")
            output.write(f"ANSWER: {answers_list[iter-1]}\n\n")
            output.write("#### FILES AND PAGES REFERENCED ####\n")
            for file_name, page_num in files_pages_list[iter-1]:
                output.write(f"File: {file_name}, Page: {page_num}\n")
            output.write("=" * 150 + "\n\n\n")
            iter += 1

        return BytesIO(output.getvalue().encode('utf-8'))
    except:
        st.error('Error in function --> **get_text_file**')