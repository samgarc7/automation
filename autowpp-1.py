import time
import csv
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def iniciar_sessao(perfil_path, profile_name):
    options = Options()
    options.add_argument("--user-data-dir=" + perfil_path)
    options.add_argument(f"--profile-directory={profile_name}")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def enviar_mensagem(driver, numero, mensagem):
    try:
        url = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem}"
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        enviar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']")))
        enviar.click()
        time.sleep(10)
    except Exception as e:
        print(f'falha ao enviar mensagem para o numero: {numero} / ({mensagem}) Erro: {e}')

def enviar_mult_msg():
    perfil_path = "/Users/samuelgarciaoliveira/Library/Application Support/Google/Chrome"
    profile_name = 'Profile 8'
    driver = iniciar_sessao(perfil_path, profile_name)
    time.sleep(10)
    with open('mensagens_unificadas.csv', 'r', encoding='utf-8') as file:
        csv_read = csv.DictReader(file)     
        for id, row in enumerate(csv_read):
            mensagem = row['mensagem']
            numero = row['numero_telefone']
            enviar_mensagem(driver, numero, mensagem)
            time.sleep(random.uniform(8,12))
    driver.quit()

enviar_mult_msg()