import os
import json
from datetime import datetime

def save_log(soru, model, cevap):
    zaman = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    klasor = "loglar"
    os.makedirs(klasor, exist_ok=True)

    # Metin log
    with open(os.path.join(klasor, "log_kayitlari.txt"), "a", encoding="utf-8") as f:
        f.write(f"\n[{zaman}]\nSoru: {soru}\nModel: {model}\nCevap: {cevap}\n{'-'*50}")

    # JSON log
    kayit = {"tarih": zaman, "model": model, "soru": soru, "cevap": cevap}
    with open(os.path.join(klasor, f"{zaman}.json"), "w", encoding="utf-8") as f:
        json.dump(kayit, f, indent=2, ensure_ascii=False)
