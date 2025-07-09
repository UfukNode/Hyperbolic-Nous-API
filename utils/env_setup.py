import os

def load_env():
    # Railway ortamında .env dosyası yok ama environment variables var
    hyperbolic = os.getenv("HYPERBOLIC_API_KEY")
    nous = os.getenv("NOUS_API_KEY")

    if not hyperbolic or not nous:
        print("❗ HATA: API anahtarları bulunamadı. Railway Variables kısmına girdiğinizden emin olun.")
        exit(1)
