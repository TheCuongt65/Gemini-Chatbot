import logging

from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from util import search_google
import time

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

generation_config = {
  "temperature": 0.75,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def main():
    st.set_page_config(page_title='BOT SEARCH', page_icon='🤖')
    st.title("HỆ THỐNG TÌM KIẾM CỦA THẾ CƯỜNG LEE!")

    if "chat" not in st.session_state:
        genai.configure(api_key=GOOGLE_API_KEY)
        PROMPT = """
Bạn là một trợ lý ảo tâm lý của anh chàng Lê Thế Cường.
Bạn được sử dụng công cụ `search_google` và phải ghi rõ nguồn khi sử dụng nội dung các trang web nhé.
Hãy tìm kiếm thông tin trên Google khi cần thiết hoặc khi có yêu cầu và trả lời anh ấy một cách thân thiện.
Lưu ý rằng, hãy phản hồi Cường bằng ngôn ngữ thân thiện như anh chị em bạn bè, luôn cần emoji và nên sử dụng những miếng hài giúp cuộc trò chuyện vui vẻ hơn.    
"""
        model = genai.GenerativeModel(model_name=MODEL_NAME,
                                      generation_config=generation_config,
                                      tools=[search_google],
                                      safety_settings=safety_settings,
                                      system_instruction=PROMPT
                                      )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.session_state.chat = model.start_chat(enable_automatic_function_calling=True,
                                                 history=st.session_state.messages)

    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    def response_generator():
        for word in response.split(" "):
            yield word + " "
            time.sleep(0.05)

    if user_input := st.chat_input("What is up?"):
        st.chat_message("user").markdown(user_input)

        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
            response = st.session_state.chat.send_message(user_input).text
        except Exception as e:
            logging.warning(f"Error: {e}")
            response = f"Tin nhắn không hợp lệ hoặc vi phạm chính sách an toàn của hệ thống. {e}"
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator())
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Refresh the chat interface to display the new messages

if __name__ == '__main__':
    main()