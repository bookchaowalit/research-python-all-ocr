import os
import tempfile

import streamlit as st
from typhoon_ocr import ocr_document

st.title("Typhoon OCR Streamlit Demo")

uploaded_file = st.file_uploader(
    "Upload a PDF or image", type=["pdf", "jpg", "jpeg", "png"]
)
task_type = st.selectbox("Task Type", ["default", "structure"])

page_num = None
if uploaded_file is not None and uploaded_file.type == "application/pdf":
    page_num = st.number_input("Page Number (for PDFs)", min_value=1, value=1, step=1)

if st.button("Run OCR") and uploaded_file is not None:
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
    ) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    kwargs = {
        "pdf_or_image_path": tmp_path,
        "task_type": task_type,
    }
    if page_num is not None:
        kwargs["page_num"] = int(page_num)

    st.info("Processing...")
    markdown = ocr_document(**kwargs)
    st.markdown(markdown)
    os.remove(tmp_path)
