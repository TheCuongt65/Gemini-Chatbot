import requests

def search_medical_documents(query: str) -> str:
    """
      Hàm tìm kiếm thông tin y tế về `query`.

      Tham số:
        query: Từ khóa, cụm từ khóa để tìm kiếm.

      Trả về:
        Danh sách các kết quả tìm kiếm trong các tài liệu
    """
    url = "https://thecuong-healthy-search.hf.space/search/"
    params = {
        "query": query,
        "limit": 3,
        # "rerank": False,
        # "content": True
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=params, headers=headers)
    return response.text