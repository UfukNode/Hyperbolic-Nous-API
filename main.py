from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx

# API Key'i Railway ortam değişkenlerinden al
HYPERBOLIC_API_KEY = os.getenv("HYPERBOLIC_API_KEY")
if not HYPERBOLIC_API_KEY:
    raise ValueError("❌ HYPERBOLIC_API_KEY bulunamadı! Railway'de environment variable eklemeyi unutma.")

# Uygulama başlat
app = FastAPI(title="Hyperbolic API", version="1.0")

# CORS ayarları (her yerden istek kabul eder)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ana endpoint
@app.get("/")
async def root():
    return {"message": "✅ Hyperbolic API aktif."}

# Chat endpoint
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    if not user_message:
        return {"success": False, "error": "Mesaj alanı boş"}

    # Hyperbolic API'ye istek gönder
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.hyperbolic.xyz/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {HYPERBOLIC_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "nous-hermes-2-mixtral-8x7b-dpo",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_message}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.7
                }
            )

            result = response.json()
            return {
                "success": True,
                "response": result["choices"][0]["message"]["content"]
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
