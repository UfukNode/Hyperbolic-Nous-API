import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()

    # Railway ortamında .env yok ama değişkenler var olabilir
    hyperbolic = os.getenv("HYPERBOLIC_API_KEY")
    nous = os.getenv("NOUS_API_KEY")

    if not hyperbolic or not nous:
        print("❗ HATA: API anahtarları bulunamadı. Railway veya .env dosyanızda eksik olabilir.")
        exit(1)
