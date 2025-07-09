import os
import requests
import random

def generate_question():
    API_KEY = os.getenv("HYPERBOLIC_API_KEY")
    MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"

    # Ufuk'a özel ilgi alanlarından oluşan konu havuzu
    konular = [
        "kripto para psikolojisi", "ZK teknolojileri", "node operatörlüğü", "yapay zeka ve toplum", 
        "bilgi güvenliği", "etik hackleme", "felsefi paradokslar", "anlam arayışı", "teknoloji bağımlılığı", 
        "web3 ve geleceği", "topluluk yönetimi", "bilinçli farkındalık", "multiverse teorisi", 
        "gelecekte meslekler", "makine öğrenmesi", "sanal kimlikler", "hacker kültürü", 
        "özgür irade", "entelektüel yalnızlık", "sosyal medya etkileri"
    ]

    prompt_tarzlari = [
        "Bu konuyla ilgili kısa ama düşündürücü bir soru üret:",
        "Basit ama zekice bir soru hazırla:",
        "İlginç ve yaratıcı bir soru oluştur:",
        "Karmaşık olmayan ama özgün bir soru yaz:",
        "Yapay zeka modellerini test edecek sade bir soru oluştur:"
    ]

    secilen_konu = random.choice(konular)
    secilen_prompt = random.choice(prompt_tarzlari)
    tam_prompt = f"{secilen_prompt} '{secilen_konu}'"

    mesajlar = [
        {"role": "system", "content": "Sen kısa ama düşündürücü sorular üreten bir sistemsin. Sorular yaratıcı ve farklı olmalı."},
        {"role": "user", "content": tam_prompt}
    ]

    veri = {
        "model": MODEL,
        "messages": mesajlar,
        "max_tokens": 128,
        "temperature": 0.95,
        "top_p": 0.95
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post("https://api.hyperbolic.xyz/v1/chat/completions", headers=headers, json=veri, timeout=10)
        return res.json()["choices"][0]["message"]["content"].strip()
    except:
        return "Gerçeklik kavramı nedir ve nasıl tanımlanabilir?"
