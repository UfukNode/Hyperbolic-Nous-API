from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()

    if not os.getenv("HYPERBOLIC_API_KEY") or not os.getenv("NOUS_API_KEY"):
        print("❗HATA: API anahtarları bulunamadı. `.env` dosyanızı oluşturmayı unutmayın.")
        exit(1)
