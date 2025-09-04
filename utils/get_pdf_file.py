from io import BytesIO, StringIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import streamlit as st

from utils.questions import general_questions, shipping_logistics_questions, bid_rfi_rfp_questions


# Function to generate a PDF from text content
# Function to create PDF from data
def get_pdf_file(questions, answers_list, files_pages_list, processed_file_type, selected_file_type):
    try:
        # Check if the categories match
        if processed_file_type == "General" and questions != general_questions:
            st.warning(f"The answers below are for the **{processed_file_type}** category. Please click on **Generate Answers** button to generate answers for the **{selected_file_type}** category!")
        
        elif processed_file_type == "Shipping & Logistics" and questions != shipping_logistics_questions:
            st.warning(f"The answers below are for the **{processed_file_type}** category. Please click on **Generate Answers** button to generate answers for the **{selected_file_type}** category!")

        elif processed_file_type == "RFI/RFP (Bid)" and questions != bid_rfi_rfp_questions:
            st.warning(f"The answers below are for the **{processed_file_type}** category. Please click on **Generate Answers** button to generate answers for the **{selected_file_type}** category!")

        else:
            # Create PDF
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Add Title
            title = Paragraph("PDF QUESTION ANSWERING REPORT", styles["Title"])
            story.append(title)
            story.append(Spacer(1, 12))

            # Add content for each question
            iter = 1
            for question in questions:
                # Add question header
                question_header = Paragraph(f"QUESTION {iter}: {question.upper()}", styles["Heading2"])
                story.append(question_header)

                # Add answer
                answer_paragraph = Paragraph(f"ANSWER: {answers_list[iter-1]}", styles["BodyText"])
                story.append(answer_paragraph)
                story.append(Spacer(1, 12))

                # Add files and pages referenced
                story.append(Paragraph("FILES AND PAGES REFERENCED:", styles["Heading3"]))
                
                # Create table for file names and pages
                table_data = [["File Name", "Page Number"]] + files_pages_list[iter-1]
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ])
                table = Table(table_data)
                table.setStyle(table_style)
                story.append(table)
                story.append(Spacer(1, 24))

                # Add separator between questions
                story.append(Paragraph("=" * 150, styles["BodyText"]))
                story.append(Spacer(1, 24))

                iter += 1

            # Build the PDF
            doc.build(story)
            pdf_buffer.seek(0)  # Reset buffer pointer
            return pdf_buffer

    except Exception as e:
        st.error(f"Error in function --> **get_pdf_file**: {str(e)}")