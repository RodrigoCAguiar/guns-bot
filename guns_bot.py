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
    payload = {"chat_id": chat_id, "text": msg}

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

        # Local do show
        city_tag = panel.find("div", class_="tourLocation__city")
        if not city_tag:
            continue

        city = city_tag.get_text(strip=True)

        # procuramos Fortaleza
        if not city.startswith(TARGET_CITY):
            continue

        print(f"Show encontrado: {city}")

        # pega todos os spans (status)
        spans = panel.find_all("span")
        statuses = [s.get_text(strip=True) for s in spans if s.get_text(strip=True)]

        # envia alerta detalhado
        msg = (
            "🎸 *GUNS N' ROSES — FORTALEZA*\n"
            f"📍 Cidade: {city}\n\n"
            f"🔐 Nightrain: {statuses[0] if len(statuses) > 0 else 'N/A'}\n"
            f"🎟 Público: {statuses[1] if len(statuses) > 1 else 'N/A'}"
        )

        print(msg)
        send_telegram(msg)

        return  # finaliza pois Fortaleza já foi tratada

    print("Fortaleza não encontrada.")


if __name__ == "__main__":
    monitor()

