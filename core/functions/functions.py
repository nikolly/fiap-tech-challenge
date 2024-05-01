from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json


def config_selenium():
    options = Options()
    options.add_argument("--headless")
    
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def get_csv(driver, category, sub_option=None):
    if sub_option:
        category += f'&subopcao=subopt_{sub_option}'
        
    driver.get(f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_{category}")
    
    link_download = driver.find_element(By.CSS_SELECTOR, '.footer_content[href$=".csv"]')
    csv = link_download.get_attribute('href')
        
    return csv


def load_users_from_json(file_path):
    with open(file_path, "r") as file:
        users_data = json.load(file)
    return users_data
