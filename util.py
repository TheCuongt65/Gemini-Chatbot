import requests

def search_medical_documents(query: str) -> str:
    url = "https://thecuong-healthy-search.hf.space/search/"
    params = {"query": query, "limit": 3}
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url, json=params, headers=headers)
    return response.text