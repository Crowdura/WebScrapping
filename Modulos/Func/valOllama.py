def getListLLM():
    import requests
    url = "http://localhost:11434/api/tags"
    response = requests.get(url)
    return response.json()