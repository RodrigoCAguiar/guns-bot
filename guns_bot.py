import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.gunsnroses.com/tour"
TARGET_CITY = "Fortaleza"

def send_telegram(msg):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Telegram não configurado.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": msg,
        "parse_mode": "Markdown"   # 👉 ativa formatação
    }

    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Erro Telegram:", e)


def monitor():
    print("Verificando...")

    try:
        r = requests.get(URL, timeout=20)
        html = r.text
    except Exception as e:
        print("Erro ao baixar página:", e)
        return

    soup = BeautifulSoup(html, "html.parser")
    panels = soup.find_all("div", class_="tourListPanel")

    for panel in panels:

        city_tag = panel.find("div", class_="tourLocation__city")
        if not city_tag:
            continue

        city = city_tag.get_text(strip=True)

        if not city.startswith(TARGET_CITY):
            continue

        print(f"Show encontrado: {city}")

        spans = panel.find_all("span")
        statuses = [s.get_text(strip=True) for s in spans if s.get_text(strip=True)]

        nightrain = statuses[0] if len(statuses) > 0 else "N/A"
        publico   = statuses[1] if len(statuses) > 1 else "N/A"

        night_open = "COMING SOON" not in nightrain.upper()
        pub_open   = "COMING SOON" not in publico.upper()

        # 👉 AQUI DEFINIMOS O TÍTULO
        if night_open or pub_open:
            titulo = "🚨 *INGRESSOS ABERTOS — FORTALEZA!*"
        else:
            titulo = "❌ *Ainda indisponível — Fortaleza*"

        msg = (
            f"{titulo}\n\n"
            f"🎸 *GUNS N' ROSES — FORTALEZA*\n"
            f"📍 *Cidade:* `{city}`\n\n"
            f"🔐 *Nightrain:* `{nightrain}`\n"
            f"🎟 *Público:* `{publico}`\n\n"
            f"🔗 [Acessar página oficial](https://www.gunsnroses.com/tour)"
        )

        print(msg)
        send_telegram(msg)
        return

    print("Fortaleza não encontrada.")


if __name__ == "__main__":
    monitor()
