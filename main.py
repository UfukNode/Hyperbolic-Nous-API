from core.generator import generate_question
from core.responder import get_nous_response
from core.logger import save_log
from utils.cli import choose_models
from utils.env_setup import load_env
import time
import os

class Renk:
    MAVI = '\033[94m'
    YESIL = '\033[92m'
    SARI = '\033[93m'
    KIRMIZI = '\033[91m'
    RESET = '\033[0m'

BEKLEME_SANIYE = 30

def main():
    load_env()

    print(Renk.MAVI + "Başlatılıyor..." + Renk.RESET)
    print(Renk.SARI + "Nous modellerini seçin ve her model için rastgele üretilen sorularla cevaplarını kıyaslayın.\n" + Renk.RESET)

    modeller = choose_models()

    while True:
        soru = generate_question()
        print(Renk.MAVI + f"\nSoru: {soru}\n" + Renk.RESET)

        for model in modeller:
            print(Renk.SARI + f"Model: {model} yanıtlıyor..." + Renk.RESET)
            yanit = get_nous_response(model, soru)

            if yanit:
                print(Renk.YESIL + f"\nCevap:\n{yanit}\n" + Renk.RESET)
                save_log(soru, model, yanit)
            else:
                print(Renk.KIRMIZI + "Cevap alınamadı veya hata oluştu.\n" + Renk.RESET)

            print(Renk.SARI + f"{BEKLEME_SANIYE} saniye bekleniyor...\n" + Renk.RESET)
            time.sleep(BEKLEME_SANIYE)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Renk.KIRMIZI + "\nProgram kullanıcı tarafından durduruldu." + Renk.RESET)
    except Exception as e:
        print(Renk.KIRMIZI + f"\nBeklenmeyen bir hata oluştu: {e}" + Renk.RESET)
