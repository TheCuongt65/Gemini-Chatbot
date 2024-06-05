from chatbot import ChatBot
import streamlit as st
import time

def main():
    st.set_page_config(page_title='ChatBot AI', page_icon='🤖')

    st.title("Gemini - Chat with documents")
    pdf = st.file_uploader("Upload your .doc or .pdf", type=['pdf', 'docx'])
    chatbot = ChatBot()
    chatbot.set_doc(pdf)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    def response_generator():
        for word in response.split(" "):
            yield word + " "
            time.sleep(0.05)

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = chatbot.respond_chat(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator())
        # Add assistant response to chat history
        # st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == '__main__':
    main()