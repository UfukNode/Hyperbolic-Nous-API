from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
import uvicorn
import asyncio
import random
import time
from datetime import datetime

HYPERBOLIC_API_KEY = os.getenv("HYPERBOLIC_API_KEY")
PORT = int(os.getenv("PORT", 8000))
COOLDOWN_SECONDS = 30
MAX_TOKENS_HYPERBOLIC = 128
MAX_TOKENS_NOUS = 256

if not HYPERBOLIC_API_KEY:
    raise ValueError("HYPERBOLIC_API_KEY bulunamadı!")

app = FastAPI(title="Hyperbolic Nous Otomatik Test API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NOUS_MODELS = [
    "nous-hermes-2-mixtral-8x7b-dpo",
    "meta-llama/Meta-Llama-3-70B-Instruct",
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "meta-llama/Meta-Llama-3.1-405B-Instruct"
]

QUESTION_TOPICS = [
    "yapay zeka ve makine öğrenmesi",
    "uzay keşfi ve Mars kolonizasyonu", 
    "yenilenebilir enerji ve sürdürülebilirlik",
    "kuantum bilgisayar ve fizik",
    "biyoteknoloji ve genetik mühendisliği",
    "felsefe ve bilinç",
    "iklim değişikliği ve çevre bilimi",
    "robotik ve otomasyon",
    "kripto para ve blockchain",
    "sanal gerçeklik ve metaverse"
]

class OtomatikTester:
    def __init__(self):
        self.current_model_index = 0
        self.running = False
    
    async def soru_uret(self, konu: str) -> str:
        prompts = [
            f"{konu} hakkında düşündürücü bir soru oluştur. Spesifik ve ilginç olsun.",
            f"{konu} ile ilgili derin analiz gerektiren karmaşık bir soru yarat.",
            f"{konu} hakkında gelecek olasılıklarını keşfeden yenilikçi bir soru sor.",
            f"{konu} hakkında anlayışı test eden zorlu bir soru formüle et.",
        ]
        
        selected_prompt = random.choice(prompts)
        
        async with httpx.AsyncClient(timeout=30.0) as client:
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
                            {"role": "system", "content": "Sen bir soru üreticisisin. Sadece soruyu üret, ek metin yazma."},
                            {"role": "user", "content": selected_prompt}
                        ],
                        "max_tokens": MAX_TOKENS_HYPERBOLIC,
                        "temperature": 0.8
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    question = result["choices"][0]["message"]["content"].strip()
                    print(f"Üretilen soru: {question}")
                    return question
                else:
                    print(f"Soru üretimi başarısız: {response.status_code}")
                    return f"{konu} konusunun gelecek on yıldaki etkileri nelerdir?"
                    
            except Exception as e:
                print(f"Soru üretimi hatası: {str(e)}")
                return f"{konu} konusunun temel kavramlarını açıklayın."
    
    async def modele_sor(self, model: str, question: str) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    "https://api.hyperbolic.xyz/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {HYPERBOLIC_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "Sen yardımcı bir asistansın. Detaylı ve düşünceli cevaplar ver."},
                            {"role": "user", "content": question}
                        ],
                        "max_tokens": MAX_TOKENS_NOUS,
                        "temperature": 0.7
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"].strip()
                    
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"\n{'='*80}")
                    print(f"Model: {model}")
                    print(f"Zaman: {timestamp}")
                    print(f"Soru: {question}")
                    print(f"Cevap: {answer}")
                    print(f"Kullanılan Token: ~{len(answer.split())}")
                    print(f"{'='*80}\n")
                    
                    return answer
                else:
                    print(f"Model {model} başarısız: {response.status_code}")
                    return f"Hata: Model {response.status_code} döndürdü"
                    
            except Exception as e:
                print(f"Model {model} ile hata: {str(e)}")
                return f"Hata: {str(e)}"
    
    async def otomatik_test_calistir(self):
        self.running = True
        print(f"Otomatik test başlatıldı! {len(NOUS_MODELS)} model test edilecek.")
        print(f"Her model arası {COOLDOWN_SECONDS} saniye bekleme...")
        
        cycle_count = 0
        
        while self.running:
            try:
                cycle_count += 1
                print(f"\nDöngü #{cycle_count} başlıyor...")
                
                topic = random.choice(QUESTION_TOPICS)
                print(f"Seçilen konu: {topic}")
                
                question = await self.soru_uret(topic)
                
                for i, model in enumerate(NOUS_MODELS):
                    if not self.running:
                        break
                        
                    print(f"\nModel testi {i+1}/{len(NOUS_MODELS)}: {model}")
                    
                    answer = await self.modele_sor(model, question)
                    
                    if i < len(NOUS_MODELS) - 1:
                        print(f"Sonraki model için {COOLDOWN_SECONDS} saniye bekleniyor...")
                        await asyncio.sleep(COOLDOWN_SECONDS)
                
                print(f"Döngü #{cycle_count} tamamlandı!")
                print(f"Sonraki döngü için 60 saniye bekleniyor...")
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"Otomatik test hatası: {str(e)}")
                await asyncio.sleep(30)

otomatik_tester = OtomatikTester()

@app.get("/")
async def ana_sayfa():
    return {
        "mesaj": "Hyperbolic Nous Otomatik Test API aktif",
        "durum": "çalışıyor" if otomatik_tester.running else "durduruldu",
        "modeller": NOUS_MODELS,
        "bekleme_suresi": COOLDOWN_SECONDS
    }

@app.post("/otomatik-test-baslat")
async def otomatik_test_baslat():
    if not otomatik_tester.running:
        asyncio.create_task(otomatik_tester.otomatik_test_calistir())
        return {"mesaj": "Otomatik test başlatıldı!", "durum": "çalışıyor"}
    else:
        return {"mesaj": "Otomatik test zaten çalışıyor", "durum": "zaten_çalışıyor"}

@app.post("/otomatik-test-durdur")
async def otomatik_test_durdur():
    otomatik_tester.running = False
    return {"mesaj": "Otomatik test durduruldu", "durum": "durduruldu"}

@app.get("/durum")
async def durum_kontrol():
    return {
        "çalışıyor": otomatik_tester.running,
        "mevcut_model": otomatik_tester.current_model_index,
        "toplam_model": len(NOUS_MODELS),
        "bekleme_saniye": COOLDOWN_SECONDS
    }

@app.post("/sohbet")
async def manuel_sohbet(request: Request):
    data = await request.json()
    kullanici_mesaji = data.get("mesaj", "")
    model = data.get("model", "nous-hermes-2-mixtral-8x7b-dpo")
    
    if not kullanici_mesaji:
        return {"basarili": False, "hata": "Mesaj alanı boş"}
    
    cevap = await otomatik_tester.modele_sor(model, kullanici_mesaji)
    return {
        "basarili": True,
        "soru": kullanici_mesaji,
        "cevap": cevap,
        "model": model
    }

if __name__ == "__main__":
    print(f"Server başlatılıyor... Port: {PORT}")
    print(f"{len(NOUS_MODELS)} model test edilmeye hazır")
    print(f"Bekleme süresi: {COOLDOWN_SECONDS} saniye")
    
    uvicorn.run(
        app, 
        host="0.0.0.0",
        port=PORT,
        log_level="info"
    )
