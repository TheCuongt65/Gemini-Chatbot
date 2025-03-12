import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
import json

load_dotenv()

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def remove_extra_newlines(text):
    return re.sub(r'\n+', '\n', text)


def search_google(query: str) -> str:
    url = 'https://customsearch.googleapis.com/customsearch/v1'
    params = {
        'q': query,
        'key': GOOGLE_SEARCH_API_KEY,
        'cx': SEARCH_ENGINE_ID,
    }
    response = requests.get(url, params=params)

    def extract_links(search_results):
        links = []
        for item in search_results.get('items', []):
            links.append(item['link'])
        return links[:3]  # Limit to 3 results

    def fetch_article_content(url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            return " "
        soup = BeautifulSoup(response.text, 'html.parser')
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()  # Remove JavaScript and CSS
        text = soup.get_text(separator=' ')
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
        return remove_extra_newlines(text.strip())

    links = extract_links(response.json())
    article_contents = [
        f"- [{link}]({link})\n\n```\n{fetch_article_content(link)}\n```"
        for link in links
    ]
    return "\n\n".join(article_contents)


if __name__ == "__main__":
    # print(search_medical_documents("covid-19"))
    print(search_google("anh trai vượt ngàn chông gai"))