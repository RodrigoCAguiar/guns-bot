import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.gunsnroses.com/tour"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def log(msg):
    print(msg, flush=True)


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}

    try:
        r = requests.post(url, data=data, timeout=10)
        log(f"Telegram Status: {r.status_code}")
        log(f"Resposta do Telegram: {r.text}")
    except Exception as e:
        log(f"Erro ao enviar Telegram: {e}")


def verificar_ingressos():
    try:
        response = requests.get(URL, timeout=20)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        shows = soup.select(".tourListPanel")

        # DEBUG: salvar o HTML completo para inspeção
        with open("debug_fullpage.html", "w", encoding="utf-8") as f:
            f.write(html)

        encontrou_fortaleza = False

        for show in shows:
            cidade_el = show.select_one(".tourLocation__city")
            if not cidade_el:
                continue

            cidade = cidade_el.get_text(strip=True)
            log(f"ENCONTREI CIDADE: {cidade}")

            if "FORTALEZA" in cidade.upper():
                encontrou_fortaleza = True

                # DEBUG: salvar apenas o bloco
                with open("debug_fortaleza.html", "w", encoding="utf-8") as f:
                    f.write(show.prettify())

                spans = [
                    s.get_text(strip=True)
                    for s in show.find_all("span")
                    if s.get_text(strip=True)
                ]

                status_nightrain = None
                status_publico = None

                for t in spans:
                    if "NIGHTRAIN" in t.upper():
                        status_nightrain = t
                    elif "PUBLIC" in t.upper():
                        status_publico = t

                log(f"STATUS NIGHTRAIN: {status_nightrain}")
                log(f"STATUS PUBLICO:   {status_publico}")

                night_open = status_nightrain and ("COMING SOON" not in status_nightrain.upper())
                pub_open = status_publico and ("COMING SOON" not in status_publico.upper())

                if night_open or pub_open:
                    alerta = (
                        "⚠️ INGRESSOS ABERTOS!\n\n"
                        f"NightTrain: {status_nightrain}\n"
                        f"Publico:    {status_publico}\n"
                        "Link: https://www.gunsnroses.com/tour"
                    )
                    send_telegram(alerta)
                else:
                    log("Ainda indisponivel.")

                return

        if not encontrou_fortaleza:
            log("⚠️ Fortaleza não encontrada! Salvando fullpage para debug.")

    except Exception as e:
        log(f"Erro: {e}")


verificar_ingressos()
