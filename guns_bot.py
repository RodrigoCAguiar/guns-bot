from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

URL = "https://www.gunsnroses.com/tour"

def log(msg):
    print(msg, flush=True)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def verificar_ingressos():
    driver = get_driver()
    driver.get(URL)
    time.sleep(6)

    shows = driver.find_elements(By.CLASS_NAME, "tourListPanel")
    log(f"Blocos encontrados: {len(shows)}")

    encontrou = False

    for show in shows:
        try:
            cidade_el = show.find_element(By.CLASS_NAME, "tourLocation__city")
            cidade = cidade_el.text.strip()

            log(f"Verificando cidade: {cidade}")

            if "Fortaleza" in cidade:
                encontrou = True
                log(f"SHOW ENCONTRADO: {cidade}")

                spans = show.find_elements(By.TAG_NAME, "span")
                textos = [s.text.strip() for s in spans if s.text.strip()]
                log(f"Status atual: {textos}")

                if any("COMING SOON" not in t for t in textos):
                    log("INGRESSOS DISPONIVEIS!")
                else:
                    log("Nada.")

                break

        except Exception as e:
            log(f"Erro lendo bloco: {e}")

    if not encontrou:
        log("Fortaleza nao encontrada neste ciclo.")

    driver.quit()


if __name__ == "__main__":
    while True:
        log("Verificando...\n")
        verificar_ingressos()
        time.sleep(60)
