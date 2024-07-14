import os
import google.generativeai as genai
from util import search_medical_documents
from dotenv import load_dotenv
# import streamlit as st

load_dotenv()
# GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
# MODEL_NAME = st.secrets["MODEL_NAME"]

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

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
Trợ lý ảo một hệ thống trả lời các câu hỏi có liên quan đến thông tin y tế cho người dùng. 
Khách hàng tên là Lê Thê Cường.
Điều này có thể bao gồm việc:
    + Tìm kiếm thông tin y tế từ công cụ tìm kiếm `search_medical_documents`
    + Trả lời các câu hỏi cho người dùng
    + Trò chuyện với người dùng
Lưu ý rằng, trợ lý ảo y tế chỉ trả lời người dùng trong pham vi bao hàm liên quan đến các lĩnh vực về y tế.
"""
        self.model = genai.GenerativeModel(model_name=self.model_name,
                                           generation_config=generation_config,
                                           tools=[search_medical_documents],
                                           safety_settings=safety_settings,
                                           system_instruction=PROMPT)
        self.token_count = self.model.count_tokens(PROMPT).total_tokens
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def respond_chat(self, user_input):
        user_input = user_input

        tokens_in_input = self.model.count_tokens(user_input).total_tokens

        if self.token_count > 1000000:
            return "Quá số lượng Token cho phép"


        response = self.chat.send_message(user_input)
        print(response)
        self.token_count += tokens_in_input + self.model.count_tokens(response.text).total_tokens
        return response.text


if __name__ == '__main__':
    obj1 = ChatBot()
    print(obj1.respond_chat('Chào bạn'))
