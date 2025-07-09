import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

HYPERBOLIC_API_KEY = os.getenv("HYPERBOLIC_API_KEY")
NOUS_API_KEY = os.getenv("NOUS_API_KEY")

NOUS_MODELS = [
    "Hermes-3-Llama-3.1-70B",
    "Hermes-3-Llama-3.1-405B",
    "DeepHermes-3-Llama-3-8B-Preview",
    "DeepHermes-3-Mistral-24B-Preview"
]

def generate_question():
    url = "https://api.hyperbolic.ai/v1/question"
    headers = {"Authorization": f"Bearer {HYPERBOLIC_API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json().get("question", "What is intelligence?")

def ask_nous_model(model, prompt):
    url = "https://api.nous.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {NOUS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful AI."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 256
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

while True:
    question = generate_question()
    print(f"\nQuestion: {question}\n")

    for model in NOUS_MODELS:
        print(f"Model: {model}")
        try:
            answer = ask_nous_model(model, question)
            print(answer)
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(30)

    print("\n---\n")
