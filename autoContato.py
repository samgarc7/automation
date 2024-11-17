import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def iniciar_sessao(perfil_path, profile_name):
    options = Options()
    options.add_argument("--user-data-dir=" + perfil_path)
    options.add_argument(f"--profile-directory={profile_name}")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # Conectando ao Chrome com a porta de depuração remota, mas no modo headless
    options.add_argument("--remote-debugging-port=9222")
    return driver 

def enviar_mensagem(driver, numero, mensagem, tentativas=1):
    attempt = 0
    while attempt < tentativas:
        try:
            wait = WebDriverWait(driver, 5)
            url = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem}"
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            enviar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']")))
            enviar.click()
            time.sleep(15)  # Tempo de espera após o envio da mensagem
            return  # Se a mensagem foi enviada com sucesso, sai da função
        except Exception as e:
            print(f'Falha ao enviar mensagem para o número: {numero} / ({mensagem}) Tentativa {attempt + 1} / Erro: {e}')
            attempt += 1
            time.sleep(random.uniform(5, 10))  # Espera antes de tentar novamente
    print(f"Falha persistente ao enviar mensagem para {numero}, pulando...")

def enviar_mult_msg():
    perfil_path = "/Users/samuelgarciaoliveira/Library/Application Support/Google/Chrome"
    profile_name = "Profile 1"
    driver = iniciar_sessao(perfil_path, profile_name)
    
    # Aguardar mais tempo após inicializar o navegador (exemplo de 20 segundos)
    time.sleep(20)  # Aguarda 20 segundos após iniciar o navegador antes de começar a enviar mensagens
    
    with open('contatos.csv', 'r', encoding='utf-8') as file:
        csv_read = csv.DictReader(file)
        for id, row in enumerate(csv_read):
            numero = row['telefone_1']
            mensagem = row['mensagem']
            enviar_mensagem(driver, numero, mensagem)
            time.sleep(random.uniform(10, 15))  # Tempo aleatório entre os envios das mensagens

    driver.quit()

enviar_mult_msg()