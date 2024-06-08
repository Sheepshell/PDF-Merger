import streamlit as st
from PyPDF2 import PdfMerger
import io
import re

def merge_pdfs(pdf_list):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merged_pdf = io.BytesIO()
    merger.write(merged_pdf)
    merger.close()
    merged_pdf.seek(0)
    return merged_pdf

def extract_first_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

# 标题
st.title("PDF Merger")
st.write("This app merges multiple PDF files into a single PDF file.")
st.write("Please upload the PDF files you want to merge and make sure they have a number in their name to specify the order.")

# 文件上传
pdf_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

# 按名称中的第一个数字排序
if pdf_files:
    # 提取文件名和内容
    pdf_files = sorted(pdf_files, key=lambda x: extract_first_number(x.name))[::-1]
    pdf_list = [pdf for pdf in pdf_files]
    merged_pdf = merge_pdfs(pdf_list)
    st.write("PDFs merged successfully!")
        
    # 提供下载按钮
    st.download_button(
        label="Download merged PDF",
        data=merged_pdf,
        file_name="{}.pdf".format(pdf_files[0].name.split(".pdf")[0] + "_merged"),
        mime="application/pdf"
        )
