from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

driver_path = './chromedriver.exe'
url = 'https://www.google.com/maps/place/Victoria+and+Albert+Museum/@51.4966392,-0.17218,15z/data=!4m5!3m4!1s0x0:0x9eb7094dfdcd651f!8m2!3d51.4966392!4d-0.17218'

def connect(driver_path, url):
    # Habilitar driver
    options = webdriver.ChromeOptions()
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, options=options)
    # Acceder a URL
    driver.get(url)
    # Habilitar cookies
    try:
        driver.find_element('xpath', '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button').click()
        # time.sleep(2)
    except Exception as e:
        print("Error de aceptacion de cookies")
    return driver

def get_reviews(driver):
    # Numero de reviews totales
    snumber_reviews = driver.find_element('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span').text.split(" ")[0]
    number_reviews = int(snumber_reviews.replace(".",""))
    # print(number_reviews)

    
    # print(driver.page_source)
    pass


def main():
    driver = connect(driver_path, url)
    data_raw = get_reviews(driver)
    while True:
        pass

if __name__ == "__main__":
    main()