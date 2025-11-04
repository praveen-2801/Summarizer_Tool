import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import sys

from utils.questions import general_questions, shipping_logistics_questions, bid_rfi_rfp_questions, contract_questions
from utils.load_model import load_model
from utils.embedding import load_embeddings
from utils.embed_pdf import embed_file
from utils.answer_question import answer_question, answer_question_contract, answer_question_shipping_logistics, answer_question_rfi_rfp
from utils.text_file_ans import get_text_file
from utils.docx_file_ans import get_docx_file
from utils.get_pdf_file import get_pdf_file
from docx import Document
import pandas as pd
import streamlit.components.v1 as components

load_model()
load_embeddings()


def main_app():
    try:
        ############################################### Webpage Configuration ##############################################
        st.set_page_config(page_title="PDF File Summarizer", page_icon=":page_with_curl:", layout="wide")

        main_col1, main_col2, main_col3 = st.columns([0.2, 0.4, 0.4])

        ############################################################## Wrapper for Middle Section ###########################################################################################
        with main_col2:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("tcp_logo.png", use_container_width =True)
            st.markdown("<h1 style='text-align: center;'>PDF File Summarizer</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Upload contract document(s) in PDF format</p>", unsafe_allow_html=True)
            #######################################################################################################################

            ########################################## PDF Upload #####################################################
            try:
                if "uploaded_files" not in st.session_state:
                    st.session_state.uploaded_files = None

                if "file_upload_check" not in st.session_state:
                    st.session_state.file_upload_check = False

                st.session_state.uploaded_files = st.file_uploader(
                                                    "Upload Files",
                                                    type=["pdf", "docx", "xlsx", "xls"],
                                                    accept_multiple_files=True
                                                )
            except:
                st.error('Error in file upload.')
            ########################################################################################################

            ############################################### Adding Chunks and Mappings to session state ################################################
            # Process each uploaded PDF and add to FAISS index
            if "all_chunks" not in st.session_state:
                st.session_state.all_chunks = []  # Store all chunks from all PDFs

            if 'all_file_page_mappings' not in st.session_state:
                st.session_state.all_file_page_mappings = []  # Store file and page mappings for all PDFs
            ####################################################################################################################

            if 'files_processed_check' not in st.session_state:
                st.session_state.files_processed_check = False

            if 'file_type_check' not in st.session_state:
                st.session_state.file_type_check = None

            ############################################## Create Embedding from the uploaded PDFs ##########################################
            try:
                #button_col1, button_col2 = st.columns(2)
                #with button_col1:
                st.info("Please click on **Process Files** button to process if new file(s) are uploaded and then go on and generate the answers.")
                if st.button('Process Files'):
                    if st.session_state.uploaded_files :
                        for uploaded_file in st.session_state.uploaded_files:
                            with st.spinner(f"Processing {uploaded_file.name}..."):
                                #if 'embed_check' not in st.session_state:
                                cchunks, file_page_mapping = embed_file(uploaded_file, uploaded_file.name)
                                    #st.session_state.embed_check = True
                                    #st.session_state.chunks = chunks
                                    #st.session_state.file_page_mapping = file_page_mapping
                                st.session_state.chunks = cchunks
                                st.session_state.file_page_mapping = file_page_mapping
                                st.session_state.all_chunks.extend(st.session_state.chunks)
                                st.session_state.all_file_page_mappings.extend(st.session_state.file_page_mapping)
                                #st.write(f'Processed file: {uploaded_file.name}')

                        st.success("All PDFs have been processed and indexed.")
                        st.session_state.files_processed_check = True
                        #st.write(st.session_state.all_file_page_mappings)
            except:
                st.error('Error in creating embeddings.')

            file_types = ['General', 'Shipping & Logistics', 'RFI/RFP (Bid)', 'Contract']
            selected_file_type = st.selectbox('Select File Type', file_types)
            #############################################################################################################################

        ################################################################################## Wrapper for Middle Section End ###############################################################

        ################################################################################## Wrapper for Left Section Start ####################################################################
        with main_col1:
            try:
                if st.session_state.files_processed_check:
                    # # Display the uploaded files in a selection box
                    # pdf_file_names = [uploaded_file.name for uploaded_file in uploaded_files]
                    # pdf_file_names.insert(0, "Select PDF File")
                    # selected_pdf = st.selectbox("Select a PDF to view", pdf_file_names)

                    # # Retrieve the selected PDF file
                    # selected_file = None
                    # for uploaded_file in uploaded_files:
                    #     if uploaded_file.name == selected_pdf:
                    #         selected_file = uploaded_file
                    #         break

                    text_question = st.text_area("Enter your question", value = "")

                    text_question_list = [text_question]

                    if st.button('Generate Answer') and text_question:
                        answers_list_side, files_pages_list_side = answer_question(text_question_list, st.session_state.all_chunks, st.session_state.all_file_page_mappings)
                        # st.session_state.ans_generated_check = True
                        st.session_state.answers_list_side = answers_list_side
                        st.session_state.files_pages_list_side = files_pages_list_side
                    try:
                        st.write("---")
                        st.write("**Answer:**")
                        st.write(st.session_state.answers_list_side[0])
                        st.write("---")
                        st.write("**Reference(s):**")
                        for file_name, page_num in st.session_state.files_pages_list_side[0]:
                                st.write(f"- File: {file_name}, Page: {page_num}")
                    except:
                        pass
                        
                        #st.write(files_pages_list_side)
            
            except:
                pass

        ################################################################################## Wrapper for Left Section End ######################################################################

        ################################################################################## Wrapper for Right Section Start ####################################################################
        with main_col3:
            try:
                selected_file = None  # initialize to avoid "not defined" error

                if st.session_state.uploaded_files:
                    # Display the uploaded files in a selection box
                    file_names = [uploaded_file.name for uploaded_file in st.session_state.uploaded_files]
                    file_names.insert(0, "Select a File")
                    selected_file_name = st.selectbox("Select a File to view", file_names)

                    if selected_file_name != "Select a File":  # only process when user picks a real file
                        for uploaded_file in st.session_state.uploaded_files:
                            if uploaded_file.name == selected_file_name:
                                selected_file = uploaded_file
                                break

                # Display the selected file
                if selected_file:
                    st.subheader(f"Viewing File: {selected_file_name}")
                    
                    if selected_file_name.lower().endswith(".pdf"):
                        pdf_bytes = selected_file.read()
                        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
                    
                        pdf_html = f"""
                            <embed
                                src="data:application/pdf;base64,{pdf_base64}"
                                type="application/pdf"
                                width="100%"
                                height="1000px"
                                style="border:none;"
                            />
                        """
                    
                        st.markdown(pdf_html, unsafe_allow_html=True)


                    elif selected_file_name.lower().endswith(".docx"):

                        doc = Document(selected_file)
                        st.markdown("### Document Content")
                        for para in doc.paragraphs:
                            if para.text.strip():
                                st.write(para.text)

                    elif selected_file_name.lower().endswith((".xlsx", ".xls")):

                        try:
                            excel_data = pd.read_excel(selected_file, sheet_name=None)  # read all sheets
                            for sheet, df in excel_data.items():
                                st.markdown(f"### Sheet: {sheet}")
                                st.dataframe(df)
                        except Exception as e:
                            st.error(f"Error reading Excel file: {e}")

            except Exception as e:
                st.error(f"Error displaying file: {e}")


        ######################################### Making only the second column scrollable ######################################
        css = '''
        <style>
            section.main>div {
                padding-bottom: 1rem;
            }
            /* Target only the second column to make it scrollable */
            [data-testid="stColumn"]:nth-child(2) > div > div {
                overflow-y: auto;
                max-height: 90vh;  /* Allow scrolling when content overflows */
            }
        </style>
        '''

        # Inject the CSS into the Streamlit app
        st.markdown(css, unsafe_allow_html=True)
        ######################################### Making only the second column scrollable ######################################


        ################################################################################## Wrapper for Right Section End ######################################################################


        ########################################################################## Second Wrapper for Middle Section Start #####################################################################
        with main_col2:
            if st.session_state.uploaded_files:
                ############################################### Generate Answers ##################################
                try:
                    #with button_col2:
                        #if 'ans_generated_check' not in st.session_state:
                        if st.button("Generate Answers for Selected File Type"):
                            st.session_state.file_type_check = selected_file_type
                            if selected_file_type == "General":
                                answers_list, files_pages_list = answer_question(general_questions, st.session_state.all_chunks, st.session_state.all_file_page_mappings)
                                st.session_state.ans_generated_check = True
                                st.session_state.answers_list = answers_list
                                st.session_state.files_pages_list = files_pages_list

                            elif selected_file_type == "Shipping & Logistics":
                                answers_list, files_pages_list = answer_question_shipping_logistics(shipping_logistics_questions, st.session_state.all_chunks, st.session_state.all_file_page_mappings)
                                st.session_state.ans_generated_check = True
                                st.session_state.answers_list = answers_list
                                st.session_state.files_pages_list = files_pages_list

                            elif selected_file_type == "RFI/RFP (Bid)":
                                answers_list, files_pages_list = answer_question_rfi_rfp(bid_rfi_rfp_questions, st.session_state.all_chunks, st.session_state.all_file_page_mappings)
                                st.session_state.ans_generated_check = True
                                st.session_state.answers_list = answers_list
                                st.session_state.files_pages_list = files_pages_list

                            elif selected_file_type == "Contract":
                                answers_list, files_pages_list = answer_question_contract(contract_questions, st.session_state.all_chunks, st.session_state.all_file_page_mappings)
                                st.session_state.ans_generated_check = True
                                st.session_state.answers_list = answers_list
                                st.session_state.files_pages_list = files_pages_list
                except Exception as e:
                    pass
                    #st.error('Error in generating answers.')
                    #st.error(e)
                ####################################################################################################

                ################################################ Get Text File ####################################
                try:
                    if selected_file_type == "General":
                        text_file_ans = get_docx_file(general_questions, st.session_state.answers_list, st.session_state.files_pages_list, st.session_state.file_type_check, selected_file_type)
                    elif selected_file_type == "Shipping & Logistics":
                        text_file_ans = get_docx_file(shipping_logistics_questions, st.session_state.answers_list, st.session_state.files_pages_list, st.session_state.file_type_check, selected_file_type)
                    elif selected_file_type == "RFI/RFP (Bid)":
                        text_file_ans = get_docx_file(bid_rfi_rfp_questions, st.session_state.answers_list, st.session_state.files_pages_list, st.session_state.file_type_check, selected_file_type)
                    elif selected_file_type == "Contract":
                        text_file_ans = get_docx_file(contract_questions, st.session_state.answers_list, st.session_state.files_pages_list, st.session_state.file_type_check, selected_file_type)
                except:
                    #st.write('Error in generating text file.')
                    pass
                ###################################################################################################

                ################################################## Get PDF File ############################################
                try:
                    if selected_file_type == "General":
                        pdf_file = get_pdf_file(general_questions, st.session_state.answers_list, st.session_state.files_pages_list, st.session_state.file_type_check, selected_file_type)
                    elif selected_file_type == "Shipping & Logistics":
                        pdf_file = get_pdf_file(shipping_logistics_questions, st.session_state.answers_list, st.session_state.files_pages_list, st.session_state.file_type_check, selected_file_type)
                    elif selected_file_type == "RFI/RFP (Bid)":
                        pdf_file = get_pdf_file(bid_rfi_rfp_questions, st.session_state.answers_list, st.session_state.files_pages_list, st.session_state.file_type_check, selected_file_type)
                    elif selected_file_type == "Contract":
                        pdf_file = get_pdf_file(contract_questions, st.session_state.answers_list, st.session_state.files_pages_list, st.session_state.file_type_check, selected_file_type)
                except:
                    #st.write('Error in generating text file.')
                    pass
                ############################################################################################################

                ################################################ Display Answers ####################################
                iter = 1
                try:
                    if selected_file_type == "General":
                        selected_questions = general_questions
                    elif selected_file_type == "Shipping & Logistics":
                        selected_questions = shipping_logistics_questions
                    elif selected_file_type == "RFI/RFP (Bid)":
                        selected_questions = bid_rfi_rfp_questions
                    elif selected_file_type == "Contract":
                        selected_questions = contract_questions

                    for question in selected_questions:
                        # Display the question and answer in the Streamlit app
                        st.write(f"**Question {iter}:** {question}")
                        st.write("**Answer:**", st.session_state.answers_list[iter-1])
                        st.write("**Files and pages referenced:**")
                        for file_name, page_num in st.session_state.files_pages_list[iter-1]:
                            st.write(f"- File: {file_name}, Page: {page_num}")
                        st.write("---")  # Divider for readability
                        iter += 1
                except:
                    #st.error('Error in displaying answers.')
                    pass
                #######################################################################################################
                download_col1, download_col2 = st.columns(2)
                ############################# Text File Download Functionality #######################################
                with download_col1:
                    try:
                        # st.download_button(
                        #     label="Download Question Answers and Page References",
                        #     data=text_file_ans,
                        #     file_name="pdf_question_answers.txt",
                        #     mime="text/plain"
                        # )
                        st.download_button(
                            label="Download Question Answering Report in Word Format",
                            data=text_file_ans,  # Coming from the BytesIO object from get_docx_file()
                            file_name=f"Summarization for {selected_file_type}.docx",  # Update to .docx
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"  # Correct MIME type for .docx
                        )
                    except:
                        #st.write('Error in downloading the file.')
                        pass
                ########################################################################################################
                ################################ PDF File Download Functionality ##########################################
                with download_col2:
                    try:
                        # Decode the BytesIO content to a string
                        #text_content = text_file_ans.getvalue().decode('utf-8', errors='replace')
                        #pdf_file = get_pdf_file(text_content)
                        st.download_button(
                            label="Download Question Answering Report in PDF Format",
                            data=pdf_file,  # BytesIO object containing PDF
                            file_name=f"Summarization for {selected_file_type}.pdf", 
                            mime="application/pdf"  # Correct MIME type for PDF
                        )
                    except Exception as e:
                        #st.error(e)
                        pass
                ############################################################################################################

        ############################################################################## Second Wrapper for Middle Section Start ###############################################################

    except:
        st.error('Some error occurred.')


# ####################################################################### Login Functionality ###########################################################################
# def login_page():
#     ############################################### Webpage Configuration ##############################################
#     st.set_page_config(page_title="PDF File Summarizer", page_icon=":page_with_curl:", layout="centered")

#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.image("tcp_logo.png", use_container_width=True)
#     st.markdown("<h1 style='text-align: center;'>PDF File Summarizer</h1>", unsafe_allow_html=True)
#     #######################################################################################################################
#     st.write("Please enter the password to continue.")
#     password = st.text_input("Password", type="password")

#     CORRECT_PASSWORD = os.getenv("CORRECT_PASSWORD")
    
#     if st.button("Submit"):
#         if password == CORRECT_PASSWORD:
#             st.session_state["authenticated"] = True
#             st.rerun()
#         else:
#             st.error("Incorrect password. Please try again.")

# if "authenticated" not in st.session_state:
#     st.session_state["authenticated"] = False

# if st.session_state["authenticated"]:
main_app()
