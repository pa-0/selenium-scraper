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

    def addLogHeader(self, mode):
        with open('log.csv', mode='a+', newline='') as log:
            log = csv.writer(log)
            if (mode == 'az'):
                log.writerow(['name', 'price', 'link'])
            elif (mode == 'wamount'):
                log.writerow(['name', 'amount', 'price', 'link'])
            elif (mode == 'wunit'):
                log.writerow(['name', 'price', 'unit', 'link'])

    def saturnScan(self):
        self.driver.implicitly_wait(0.5)
        items = self.driver.find_elements(
            By.CSS_SELECTOR, 'div[class^="StyledCardWrapper"]')
        products = []
        for item in items:
            product = item.find_element(
                By.CSS_SELECTOR, 'p[class^="BaseTypo"]')
            print(product)
            products.append(product.text)

        print(products)
        
    def walmartScan(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'div.sans-serif.mid-gray.relative')
        print(products)
        final_products = []
        for product in products:
            name = product.find_element(By.CSS_SELECTOR, 'span.w_Au').text
            final_products.append(name.strip())
        print(final_products)

    def aldiScan(self):
        self.driver.get(
            'https://www.aldi-nord.de/sortiment/kuehlung-tiefkuehlung/fleisch/gefluegel.html')
        self.driver.implicitly_wait(0.3)
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'div.mod-article-tile')
        final_products = []
        for product in products:
            name = product.find_element(
                By.CSS_SELECTOR, 'h4 span.mod-article-tile__title').text
            final_products.append(name.strip())
        print(final_products)

    def instacartScan(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'div.css-1pc1srv-ItemCardHoverProvider')
        print('Scanning...')
        for product in products:
            try:
                link = product.find_element(
                    By.CSS_SELECTOR, 'a.css-er4k5d').get_attribute('href')
            except:
                link = "-"
            try:
                amount = product.find_element(
                    By.CSS_SELECTOR, 'div.css-k50pff').text
            except:
                amount = "-"
            try:
                name = product.find_element(
                    By.CSS_SELECTOR, 'div.css-9vf613').text
                price = product.find_element(
                    By.CSS_SELECTOR, 'span.css-coqxwd').text
                with open('log.csv', mode='a+', newline='') as log:
                    log = csv.writer(log)
                    log.writerow(
                        [name.strip(), amount.strip(), price.strip(), link])
            except:
                print("skipped")
        print('Scan finished!')

    def acmeScan(self):
        with open('log.csv', mode='a+', newline='') as log:
            log = csv.writer(log)
            log.writerow(['name', 'amount', 'price', 'link'])
        products = self.driver.find_elements(By.CSS_SELECTOR, 'div.product')
        print('Scanning...')
        for product in products:
            try:
                link = product.find_element(
                    By.CSS_SELECTOR, 'div.description a').get_attribute('href')
            except:
                link = "-"
            try:
                amount = product.find_element(By.CSS_SELECTOR, 'div.size').text
            except:
                amount = "-"
            try:
                price = product.find_element(
                    By.CSS_SELECTOR, 'div.price span.sale').text
            except:
                try:
                    price = product.find_element(
                        By.CSS_SELECTOR, 'div.price').text
                except:
                    price = "-"
            try:
                name = product.find_element(
                    By.CSS_SELECTOR, 'div.description a').text
                with open('log.csv', mode='a+', newline='') as log:
                    log = csv.writer(log)
                    log.writerow(
                        [name.strip(), amount.strip(), price.strip(), link])
            except:
                print("skipped")
        print('Scan finished!')

    def amazonScan(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'div.s-widget-container div.s-card-container')
        print('Scanning...')
        for product in products:
            try:
                link = product.find_element(
                    By.CSS_SELECTOR, 'h2 a.a-link-normal').get_attribute('href')
            except:
                link = "-"
            try:
                price = product.find_element(
                    By.CSS_SELECTOR, 'span.a-price-whole').text
            except:
                price = "-"
            try:
                name = product.find_element(
                    By.CSS_SELECTOR, 'span.a-size-medium').text
                with open('log.csv', mode='a+', newline='') as log:
                    log = csv.writer(log)
                    log.writerow([name.strip(), price.strip(), link])
            except:
                print("skipped")
        print('Scan finished!')

    def sellerstats(self):
        item_id = '6170053'
        self.driver.get(
            'https://sellerstats.ru/stat/product/wb/'+ item_id +'/daily/')
        print('Scanning...')
        try:
            # price = product.find_element(By.CSS_SELECTOR, '.ag-cell-value').text
            item = product.find_element(By.CSS_SELECTOR, '[data-value="csv_all"]').click()
        except:
            print("skipped")
        print('Scan finished!')

    def mediamarktScan(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'div[class^="StyledListItem"]')
        print('Scanning...')
        for product in products:
            try:
                link = product.find_element(
                    By.CSS_SELECTOR, 'a[class^=StyledLinkRouter]').get_attribute('href')
            except:
                link = "-"
            try:
                price = product.find_element(
                    By.CSS_SELECTOR, 'div[class^="StyledUnbrandedPriceDisplayWrapper"] span[aria-hidden="true"]').text
            except:
                price = "-"
            try:
                name = product.find_element(
                    By.CSS_SELECTOR, 'p[class^="BaseTypo"]').text
                with open('log.csv', mode='a+', newline='') as log:
                    log = csv.writer(log)
                    log.writerow([name.strip(), price.strip(), link])
            except:
                print("skipped")
        print('Scan finished!')

   
    def atbScan(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'article.catalog-item')
        print('Scanning...')
        for product in products:
            try:
                link = product.find_element(
                    By.CSS_SELECTOR, 'div.catalog-item__title a').get_attribute('href')
            except:
                link = "-"
            try:
                price = product.find_element(By.CSS_SELECTOR, 'div.catalog-item__product-price span:first-child').text + \
                    '.' + product.find_element(
                        By.CSS_SELECTOR, 'div.catalog-item__product-price span:first-child').text
            except:
                price = "-"
            try:
                unit = product.find_element(
                    By.CSS_SELECTOR, 'abbr.product-price__currency-abbr').text
            except:
                price = "-"
            try:
                name = product.find_element(
                    By.CSS_SELECTOR, 'div.catalog-item__title a').text
                with open('log.csv', mode='a+', newline='') as log:
                    log = csv.writer(log)
                    log.writerow(
                        [name.strip(), price.strip(), unit.strip(), link])
            except:
                print("skipped")
        print('Scan finished!')

    def auchanScan(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'div.item_wrapper__3N0Oy')
        print('Scanning...')
        for product in products:
            try:
                link = product.find_element(
                    By.CSS_SELECTOR, 'div.item_data__top__3OdLf a.item_data__name__3bRJz').get_attribute('href')
            except:
                link = "-"
            try:
                price = product.find_element(
                    By.CSS_SELECTOR, 'div.item_price__sEYUp span').text
            except:
                price = "-"
            try:
                name = product.find_element(
                    By.CSS_SELECTOR, 'div.item_data__top__3OdLf a.item_data__name__3bRJz').text
                with open('log.csv', mode='a+', newline='') as log:
                    log = csv.writer(log)
                    log.writerow([name.strip(), price.strip(), link])
            except:
                print("skipped")
        print('Scan finished!')

    def ottoScan(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'article.product')
        print('Scanning...')
        for product in products:
            try:
                link = product.find_element(
                    By.CSS_SELECTOR, 'a.find_tile__productLink').get_attribute('href')
            except:
                link = "-"
            try:
                price = product.find_element(
                    By.CSS_SELECTOR, 'span.find_tile__priceValue').text
            except:
                price = "-"
            try:
                name = product.find_element(
                    By.CSS_SELECTOR, 'h2.find_tile__name').text
                with open('log.csv', mode='a+', newline='') as log:
                    log = csv.writer(log)
                    log.writerow([name.strip(), price.strip(), link])
            except:
                print("skipped")
        print('Scan finished!')

    def silpoScan(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'div.product-list-item')
        print('Scanning...')
        for product in products:
            try:
                link = product.find_element(
                    By.CSS_SELECTOR, 'a.image-content-wrapper').get_attribute('href')
            except:
                link = "-"
            try:
                price = product.find_element(
                    By.CSS_SELECTOR, 'div.price-wrapper div.current-integer').text
            except:
                price = "-"
            try:
                amount = product.find_element(
                    By.CSS_SELECTOR, 'div.product-weight').text
            except:
                amount = "-"
            try:
                name = product.find_element(
                    By.CSS_SELECTOR, 'div.product-title').text
                with open('log.csv', mode='a+', newline='') as log:
                    log = csv.writer(log)
                    log.writerow(
                        [name.strip(), price.strip(), amount.strip(), link])
            except:
                print("skipped")
        print('Scan finished!')

    def comfyScan(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'div.products-list-item')
        print('Scanning...')
        for product in products:
            try:
                link = product.find_element(
                    By.CSS_SELECTOR, 'a.products-list-item__name').get_attribute('href')
            except:
                link = "-"
            try:
                price = product.find_element(
                    By.CSS_SELECTOR, 'div.products-list-item__actions-price-current').text
            except:
                price = "-"
            try:
                name = product.find_element(
                    By.CSS_SELECTOR, 'a.products-list-item__name').text
                with open('log.csv', mode='a+', newline='') as log:
                    log = csv.writer(log)
                    log.writerow([name.strip(), price.strip(), link])
            except:
                print("skipped")
        print('Scan finished!')

    def foxtrotScan(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'div.sc-product')
        print('Scanning...')
        for product in products:
            try:
                link = product.find_element(
                    By.CSS_SELECTOR, 'a.card__title').get_attribute('href')
            except:
                link = "-"
            try:
                price = product.find_element(
                    By.CSS_SELECTOR, 'div.card-price').text
            except:
                price = "-"
            try:
                name = product.find_element(
                    By.CSS_SELECTOR, 'a.card__title').text
                with open('log.csv', mode='a+', newline='') as log:
                    log = csv.writer(log)
                    log.writerow([name.strip(), price.strip(), link])
            except:
                print("skipped")
        print('Scan finished!')

    def bestbuyScan(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'li.sku-item')
        print('Scanning...')
        for product in products:
            try:
                link = product.find_element(
                    By.CSS_SELECTOR, 'h4.sku-title a').get_attribute('href')
            except:
                link = "-"
            try:
                price = product.find_element(
                    By.CSS_SELECTOR, 'div.priceView-hero-price span').text
            except:
                price = "-"
            try:
                name = product.find_element(
                    By.CSS_SELECTOR, 'h4.sku-title').text
                with open('log.csv', mode='a+', newline='') as log:
                    log = csv.writer(log)
                    log.writerow([name.strip(), price.strip(), link])
            except:
                print("skipped")
        print('Scan finished!')

    def nicheArea(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 'li.search-results__list__item')
        print('Scanning...')
        for product in products:
            try:
                name = product.find_element(
                    By.CSS_SELECTOR, 'div.search-result__title-wrapper h2').text
            except:
                name = "-"
            try:
                population = product.find_element(
                    By.CSS_SELECTOR, 'li.search-result-fact-list__item p').text
            except:
                population = "-"
            try:
                rating = product.find_element(
                    By.CSS_SELECTOR, 'div.niche__grade').text
                # rating = product.find_element(
                #     By.CSS_SELECTOR, 'div.review__stars span').get_attribute('class')
            except:
                rating = "-"
            try:
                with open('log.csv', mode='a+', newline='') as log:
                    log = csv.writer(log)
                    log.writerow([name.strip(), population.strip().replace('\n', ''), rating.strip()])
            except:
                print("skipped")
        print('Scan finished!')

    generic_atb = {
        'product': 'article.catalog-item',
        'name': 'div.catalog-item__title a',
        'price': 'div.catalog-item__product-price span:first-child',
        'link': 'div.catalog-item__title a',
        'unit': 'abbr.product-price__currency-abbr'
    }


bot = ScraperBot()
