from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def connect(driver_path):
    options = webdriver.ChromeOptions()
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, options=options)
    return driver

def get_reviews(driver, url):
    return driver.get(url)

def main():
    driver = connect('./chromedriver.exe')
    data_raw = get_reviews(driver, 'https://www.google.com/maps/place/Central+Park+Zoo/@40.7712318,-73.9674707,15z/data=!3m1!5s0x89c259a1e735d943:0xb63f84c661f84258!4m16!1m8!3m7!1s0x89c258faf553cfad:0x8e9cfc7444d8f876!2sTrump+Tower!8m2!3d40.7624284!4d-73.973794!9m1!1b1!3m6!1s0x89c258f1fcd66869:0x65d72e84d91a3f14!8m2!3d40.767778!4d-73.9718335!9m1!1b1?hl=en&hl=en')
    while True:
        pass

if __name__ == "__main__":
    main()