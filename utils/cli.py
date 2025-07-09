def choose_models():
    modeller = [
        "DeepHermes-3-Mistral-24B-Preview",
        "Hermes-3-Llama-3.1-70B",
        "DeepHermes-3-Llama-3-8B-Preview",
        "Hermes-3-Llama-3.1-405B"
    ]

    print("Kullanılabilir Modeller:")
    for i, m in enumerate(modeller):
        print(f"[{i+1}] {m}")

    secim = input("Kullanmak istediğiniz modelleri seçin (virgülle ayırın veya boş bırak tümü için): ")
    if not secim.strip():
        return modeller

    indeksler = [int(i)-1 for i in secim.split(",") if i.strip().isdigit()]
    return [modeller[i] for i in indeksler if 0 <= i < len(modeller)]
