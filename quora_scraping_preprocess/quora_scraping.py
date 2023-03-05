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

# url = 'https://www.quora.com/Are-H-M-clothes-good-quality'
# csv_path = 'quora.csv'

url = 'https://www.quora.com/What-do-you-think-of-the-fashion-brand-H-M'
csv_path = 'quora2.csv'


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
        # time.sleep(3)
    except Exception as e:
        print("Error de aceptacion de cookies (quiza las cookies ya esten aceptadas)")
        # print(e)
    return driver


def load_answers(driver, file_name):

    print("CLICKING OVER MORE")
    buttons = driver.find_elements(By.CLASS_NAME, 'puppeteer_test_read_more_button')

    for button in buttons:
        time.sleep(3)
        driver.execute_script("arguments[0].click();", button)


    print("ANSWERS")
    answers = driver.find_elements(By.CSS_SELECTOR,".q-box.spacing_log_answer_content.puppeteer_test_answer_content")
    answers_list = []
    for answer in answers:
        answer_text = answer.text.replace('\n',' ')
        answers_list.append(answer_text)
        print(answer_text)

    serie_quora = pd.Series(answers_list)
    serie_quora.to_csv(file_name, index=False, sep='|')

    print(serie_quora.head())



def main():
    driver = connect(driver_path, url)
    load_answers(driver, csv_path)
    while True:
        pass
    # print("FIN")
    # time.sleep(10)



if __name__ == "__main__":
    main()
