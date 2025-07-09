import os
import requests

def get_nous_response(model, question):
    API_KEY = os.getenv("NOUS_API_KEY")
    url = "https://inference-api.nousresearch.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    veri = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Sen yardımcı ve kısa cevaplar veren bir yapay zekasın."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 256
    }

    try:
        res = requests.post(url, headers=headers, json=veri)
        return res.json()["choices"][0]["message"]["content"].strip()
    except:
        return None
