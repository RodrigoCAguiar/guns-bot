import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.gunsnroses.com/tour"

def enviar_alerta_telegram(mensagem):
    """Envia uma mensagem para o Telegram usando a API."""
    # 1. Carrega as chaves do GitHub Secrets
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not token or not chat_id:
        log("ERRO: Token ou Chat ID do Telegram não configurados nas Secrets do GitHub.")
        return

    # 2. Define o endpoint da API do Telegram
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # 3. Prepara o payload (o conteúdo da mensagem)
    payload = {
        'chat_id': chat_id,
        'text': mensagem,
        'parse_mode': 'Markdown' # Permite formatação em negrito, etc.
    }

    try:
        # 4. Envia a requisição POST
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        log("✅ Alerta de Telegram enviado com sucesso!")
    except Exception as e:
        log(f"❌ Falha ao enviar alerta para o Telegram: {e}")

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

                log(f"STATUS NIGHTRAIN: {status_nightrain}")
                log(f"STATUS PUBLICO:   {status_publico}")

                night_open = status_nightrain and ("COMING SOON" not in status_nightrain.upper())
                pub_open   = status_publico and ("COMING SOON" not in status_publico.upper())

                if night_open or pub_open:
                    log("⚠️ INGRESSOS ABERTOS!")

                else:
                    log("Ainda indisponivel.")

                return  # ENCERRA O SCRIPT DEPOIS DE UMA VERIFICAÇÃO

        # Se não achou o bloco da cidade
        log("Fortaleza nao encontrada.")

    except Exception as e:
        log(f"Erro: {e}")

# EXECUTA APENAS UMA VEZ
verificar_ingressos()

