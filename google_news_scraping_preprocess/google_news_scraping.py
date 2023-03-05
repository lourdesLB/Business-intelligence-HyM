from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from math import floor
import pandas as pd

driver_path = '../chromedriver.exe'
url = 'https://news.google.com/search?q=%22h%26m%22&hl=es&gl=ES&ceid=ES%3Aes'
csv_name = 'google_news_spanish.csv'


def connect(driver_path, url):
    # Habilitar driver
    options = webdriver.ChromeOptions()
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, options=options)
    # Acceder a URL
    try:
        driver.get(url)
    except Exception as e:
        print("No se puede acceder a la URL")
        print(e)
    # Habilitar cookies
    try:
        driver.find_element('xpath', '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button').click()
        # time.sleep(3)
    except Exception as e:
        print("Error de aceptacion de cookies (quiza las cookies ya esten aceptadas)")
        print(e)
    return driver


def load_news(driver, file_name):

    titulos = driver.find_elements(By.CLASS_NAME, 'DY5T1d')
    titulos_list = [titulo.text for titulo in titulos]
    print(titulos_list)

    news = pd.Series(titulos_list)
    news.to_csv(file_name, index=False)

    print(news.head())


def main():
    driver = connect(driver_path, url)
    load_news(driver, csv_name)
    time.sleep(10)



if __name__ == "__main__":
    main()