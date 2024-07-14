import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def search_medical_documents(query: str) -> str:
    url = "https://thecuong-healthy-search.hf.space/search/"
    params = {"query": query, "limit": 3}
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url, json=params, headers=headers)
    return response.text

def generate_response(user_input: str, chat) -> str:
    response = chat.send_message(user_input)
    return response.text