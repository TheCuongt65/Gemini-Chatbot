import os
import google.generativeai as genai
from util import read_document
# from dotenv import load_dotenv
import streamlit as st

# load_dotenv()
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
MODEL_NAME = st.secrets["MODEL_NAME"]

generation_config = {
  "temperature": 0.05,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

class ChatBot:
    def __init__(self):
        self.model_name = MODEL_NAME
        self.file = None
        self.token_count = None
        self.model = None
        self.doc = ''
        self.chat = None
        self._setup()



    def _setup(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        PROMPT = f"""
Bạn là một hệ thống trả lời các câu hỏi có liên quan đến tài liệu cho người dùng.
Điều này có thể bao gồm việc:
  + Tìm kiếm thông tin cụ thể trong tài liệu
  + Tóm tắt nội dung theo yêu cầu
  + Giải thích các khái niệm hoặc thông tin phức tạp
  + Đề xuất giúp chỉnh sửa và cải thiện nội dung của tài liệu.

Đây là tài liệu từ người dùng cung cấp:

```
{self.doc}
```
"""
        self.model = genai.GenerativeModel(model_name=self.model_name,
                                           generation_config=generation_config,
                                           safety_settings=safety_settings,
                                           system_instruction=PROMPT)
        self.token_count = self.model.count_tokens(PROMPT).total_tokens
        self.chat = self.model.start_chat()

    def set_doc(self, file):
        self.doc = read_document(file)
        self._setup()

    def respond_chat(self, user_input):
        user_input = user_input
        if user_input.lower() == "q":
            return 'Cảm ơn đã dùng dịch vụ !!!'

        tokens_in_input = self.model.count_tokens(user_input).total_tokens

        if self.token_count > 1000000:
            return "Quá số lượng Token cho phép"


        response = self.chat.send_message(user_input)
        self.token_count += tokens_in_input + self.model.count_tokens(response.text).total_tokens

        return response.text


if __name__ == '__main__':
    obj1 = ChatBot()
    print(obj1.respond_chat('Chào bạn'))
    # with open('D:\English\REPORTED SPEECH.docx', 'r') as file:
    #     print(read_document(file))
