from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
import uvicorn
from typing import Dict, Any
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
HYPERBOLIC_API_KEY = os.getenv("HYPERBOLIC_API_KEY")
PORT = int(os.getenv("PORT", 8000))  # Railway otomatik PORT atar

# API Key kontrolü
if not HYPERBOLIC_API_KEY:
    logger.error("❌ HYPERBOLIC_API_KEY bulunamadı!")
    raise ValueError("❌ HYPERBOLIC_API_KEY bulunamadı! Railway'de environment variable eklemeyi unutma.")

# Uygulama başlat
app = FastAPI(
    title="Hyperbolic Nous API", 
    version="1.0",
    description="Hyperbolic AI ile güçlendirilmiş chat API"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "✅ Hyperbolic Nous API aktif.",
        "status": "healthy",
        "version": "1.0"
    }

# Health endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "hyperbolic-nous-api"}

# Chat endpoint
@app.post("/chat")
async def chat(request: Request):
    try:
        # Request body'yi al
        data = await request.json()
        user_message = data.get("message", "")
        
        # Input validation
        if not user_message or not user_message.strip():
            raise HTTPException(
                status_code=400, 
                detail="Mesaj alanı boş veya geçersiz"
            )
        
        # Model ve diğer parametreleri al (opsiyonel)
        model = data.get("model", "nous-hermes-2-mixtral-8x7b-dpo")
        max_tokens = data.get("max_tokens", 1000)
        temperature = data.get("temperature", 0.7)
        system_message = data.get("system_message", "You are a helpful assistant.")
        
        logger.info(f"Chat request received: {user_message[:100]}...")
        
        # Hyperbolic API'ye istek gönder
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.hyperbolic.xyz/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {HYPERBOLIC_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message}
                    ],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            
            # Response kontrolü
            if response.status_code != 200:
                logger.error(f"Hyperbolic API error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Hyperbolic API hatası: {response.text}"
                )
            
            result = response.json()
            
            # Response validation
            if "choices" not in result or not result["choices"]:
                raise HTTPException(
                    status_code=500,
                    detail="API'den geçersiz yanıt alındı"
                )
            
            ai_response = result["choices"][0]["message"]["content"]
            logger.info("Chat response generated successfully")
            
            return {
                "success": True,
                "response": ai_response,
                "model": model,
                "usage": result.get("usage", {})
            }
            
    except httpx.TimeoutException:
        logger.error("Timeout error occurred")
        raise HTTPException(
            status_code=504, 
            detail="API isteği zaman aşımına uğradı"
        )
    except httpx.RequestError as e:
        logger.error(f"Request error: {str(e)}")
        raise HTTPException(
            status_code=503, 
            detail=f"API bağlantı hatası: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Beklenmeyen hata: {str(e)}"
        )

# Modelleri listele endpoint
@app.get("/models")
async def list_models():
    """Mevcut modelleri listele"""
    models = [
        "nous-hermes-2-mixtral-8x7b-dpo",
        "meta-llama/Meta-Llama-3-70B-Instruct",
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "meta-llama/Meta-Llama-3.1-70B-Instruct"
    ]
    return {"models": models}

# Chat streaming endpoint (gelişmiş)
@app.post("/chat/stream")
async def chat_stream(request: Request):
    """Streaming chat endpoint"""
    try:
        data = await request.json()
        user_message = data.get("message", "")
        
        if not user_message or not user_message.strip():
            raise HTTPException(status_code=400, detail="Mesaj alanı boş")
        
        model = data.get("model", "nous-hermes-2-mixtral-8x7b-dpo")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.hyperbolic.xyz/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {HYPERBOLIC_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_message}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.7,
                    "stream": True
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"API hatası: {response.text}"
                )
            
            # Stream response'u handle et
            full_response = ""
            async for chunk in response.aiter_lines():
                if chunk:
                    full_response += chunk
            
            return {"success": True, "response": full_response}
            
    except Exception as e:
        logger.error(f"Stream error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Railway için server başlatma
if __name__ == "__main__":
    logger.info(f"🚀 Server başlatılıyor... Port: {PORT}")
    uvicorn.run(
        app, 
        host="0.0.0.0",  # Railway için gerekli
        port=PORT,       # Railway'in atadığı port
        log_level="info"
    )
