import streamlit as st
import pdfplumber
import pandas as pd
import io

def extract_table_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        # Extract the first page
        first_page = pdf.pages[0]
        # Extract tables from the first page
        tables = first_page.extract_tables()
        # Assuming there's only one table on the first page
        if tables:
            return tables[0]
        else:
            return None

st.title("PDF to Excel Converter")
st.subheader('With using PdfPlumber to extract tables out of the uploaded PDF')
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    st.write("### Extracted Table from PDF")
    table = extract_table_from_pdf(uploaded_file)
    if table is not None:
            df = pd.DataFrame(table)
            st.write(df)

            st.write("### Download Excel File")
            excel_output = io.BytesIO()
            with pd.ExcelWriter(excel_output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=True)
            excel_file = excel_output.getvalue()
            st.download_button(
                label="Download Excel",
                data=excel_file,
                file_name="extracted_table.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
            st.write("No table found in the PDF.")
else:
        st.write("Please upload a PDF file.")


