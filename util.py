import os
from docx import Document
from PyPDF2 import PdfReader

def read_document(file):
    # Kiểm tra xem tệp có tồn tại không
    if file is None:
        return ''

    # Kiểm tra xem tệp có phải là PDF hay Word
    if file.type == 'application/pdf':
        # Đọc tài liệu PDF
        reader = PdfReader(file)
        content = []
        # Đọc từng trang
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            content.append(page.extract_text())
        return '\n'.join(content)
    elif file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        # Đọc tài liệu Word
        doc = Document(file)
        content = []
        for para in doc.paragraphs:
            content.append(para.text)
        return '\n'.join(content)
    else:
        raise "Tệp không phải là PDF hoặc Word."