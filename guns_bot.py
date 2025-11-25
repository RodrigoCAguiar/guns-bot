import requests
from bs4 import BeautifulSoup
import time

URL = "https://www.gunsnroses.com/tour"

def log(msg):
    print(msg, flush=True)

def verificar_ingressos():
    try:
        response = requests.get(URL, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")

        shows = soup.select(".tourListPanel")

        for show in shows:
            cidade_el = show.select_one(".tourLocation__city")
            if not cidade_el:
                continue

            cidade = cidade_el.get_text(strip=True)

            if "Fortaleza" in cidade:
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

                # PRINTA APENAS O QUE IMPORTA
                log(f"STATUS NIGHTRAIN: {status_nightrain}")
                log(f"STATUS PUBLICO:   {status_publico}")

                night_open = status_nightrain and ("COMING SOON" not in status_nightrain.upper())
                pub_open   = status_publico and ("COMING SOON" not in status_publico.upper())

                if night_open or pub_open:
                    log("⚠️ INGRESSOS ABERTOS!\n")
                else:
                    log("Ainda indisponivel.\n")

                break

    except Exception as e:
        log(f"Erro: {e}")


if __name__ == "__main__":
    while True:
        verificar_ingressos()
        time.sleep(60)
