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

# H&M (The Cat & Fiddle Arcade)
# url = 'https://www.facebook.com/HM-2045252695742351/reviews'
# csv_name = 'facebook.csv'

# H&M (Boulevard Francisco Medina Ascencio,)
# url = 'https://www.facebook.com/HM-864963097024789/reviews/?ref=page_internal'
# csv_name = 'facebook2.csv'

# H&M (Victoria & Alfred Waterfront)
url = 'https://www.facebook.com/HM-2008699865868134/reviews/?ref=page_internal'
csv_name = 'facebook3.csv'


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
        time.sleep(3)
    except Exception as e:
        print("Error de aceptacion de cookies (quiza las cookies ya esten aceptadas)")
        print(e)
    try: 
        button = driver.find_element('xpath', '//*[@id="facebook"]/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(5)
    except Exception as e:
        print("Error de aceptacion de cookies (quiza las cookies ya esten aceptadas)")
        print(e)    
    return driver


def load_facebooks(driver, file_name):

    posts = driver.find_elements(By.CSS_SELECTOR, '.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.xdj266r')

    posts_list = [post.text.replace('\n',' ') for post in posts]
    print(posts_list)

    posts_serie = pd.Series(posts_list)
    posts_serie.to_csv(file_name, index=False)

    print(posts_serie.head())


def main():
    driver = connect(driver_path, url)
    load_facebooks(driver, csv_name)
    time.sleep(10)



if __name__ == "__main__":
    main()