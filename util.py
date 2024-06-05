import os
import requests
from docx import Document
from PyPDF2 import PdfReader
from typing import Iterable

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



def tim_kiem_thong_tin_ve_y_te(query: str) -> str:
    """
      Hàm tìm kiếm thông tin y tế về `query`.

      Tham số:
        query: Từ khóa, cụm từ khóa để tìm kiếm.

      Trả về:
        Danh sách các kết quả tìm kiếm trong các tài liệu
      """

    url = "https://nampham1106-healthcare-search.hf.space/search"
    params = {
        "query": query,
        "limit": 3,
        "rerank": False,
        "content": True
    }
    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)

    jsonn = response.json()

    text = ''
    for i in range(len(jsonn)):
        text += f'### Kết quả tìm kiếm thứ {i}: \n ' + jsonn[i]['content'] + " \n \n "

    return text