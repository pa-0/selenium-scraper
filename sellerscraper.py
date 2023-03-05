from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import csv

DRIVER_PATH = '/Users/alireza/Documents/Tools/chromedriver'
USD_EUR_RATE = 0.99

class ScraperBot():

    def __init__(self):
        service = Service(DRIVER_PATH)
        self.driver = webdriver.Chrome(service=service)

    def goTo(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.quit()

    def sellerLogin(self):
        self.driver.get('https://sellerstats.ru/login/')
        login = self.driver.find_element(By.CSS_SELECTOR, '#id_username')
        login.send_keys('Miss.evil2010@yandex.ru')
        password = self.driver.find_element(By.CSS_SELECTOR, '#id_password')
        password.send_keys('q!JW7cn4Snz4v7A')
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
        login_button.click()
    
    def getAllIds(self):
        self.driver.get('https://sellerstats.ru/stat/products')
        sleep(1)
        ids = self.driver.find_elements(By.CSS_SELECTOR, 'span.ag-cell-value').click()
        print('ids: '+ids)
        for id in ids:
            print('going to ' + id)
            self.driver.get('https://sellerstats.ru/stat/product/wb/'+ id +'/daily/')
            self.downloadItem()
            sleep(1)

    def goToItem(self):
        item_id = '6170053'
        self.driver.get(
            'https://sellerstats.ru/stat/product/wb/'+ item_id +'/daily/')
        print('Scanning...')
        # try:
        #     # price = product.find_element(By.CSS_SELECTOR, '.ag-cell-value').text
        #     item = product.find_element(By.CSS_SELECTOR, 'span[data-value="csv_all"]').click()
        # except:
        #     print("skipped")
        # print('Scan finished!')

    def downloadItem(self):
        self.driver.find_element(By.CSS_SELECTOR, 'ul[id=help_button_download] a.dropdown-toggle').click()
        sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, 'a[data-value="csv_all"]').click()
        print('Downloaded!')
    
    generic_atb = {
        'product': 'article.catalog-item',
        'name': 'div.catalog-item__title a',
        'price': 'div.catalog-item__product-price span:first-child',
        'link': 'div.catalog-item__title a',
        'unit': 'abbr.product-price__currency-abbr'
    }


bot = ScraperBot()
