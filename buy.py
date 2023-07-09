import os
from time import sleep
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from matplotlib import pyplot as plt


class Buy(webdriver.Chrome):
    def __init__(self, driver_path="D:/PROJECT/chromedriver.exe", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Buy, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def visit_home_page(self):
        self.get("https://www.amazon.in/")

    def search_item_you_want(self, item_you_want):
        search_field = self.find_element(By.ID, 'twotabsearchtextbox')
        search_field.clear()
        search_field.send_keys(item_you_want)
        self.implicitly_wait(10)

    def click_search(self):
        search_button = self.find_element(By.ID, 'nav-search-submit-text')
        search_button.click()

        self.implicitly_wait(10)

    def pull_data_to_store_in_csv(self):
        product_name = []
        product_price = []
        product_reviews = []

        def next_page():
            i = 1
            # last_page = self.find_element(By.XPATH, "//span[@class='s-pagination-item s-pagination-disabled']").text
            # last_page_number = int(last_page)
            while i <= 10:
                next_button = self.find_element(By.XPATH, "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
                name = self.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
                for nm in name:
                    product_name.append(nm.text)
                price = self.find_elements(By.XPATH, "//span[@class='a-price']")
                for pr in price:
                    product_price.append(pr.text)
                number_of_reviews = self.find_elements(By.XPATH, "//div[@class='a-row a-size-small']")
                for rev in number_of_reviews:
                    product_reviews.append(rev.text)

                next_button.click()
                i = i + 1
        next_page()
        sleep(2)
        for n in product_name:
            print(n)
        print("\n")
        for ppr in product_price:
            print(ppr)
        print("\n")
        for rv in product_reviews:
            print(rv)
        print("\n")
        sleep(2)
        data = {'Product Name': product_name, 'Product Price': product_price, 'Total Reviews': product_reviews}
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.transpose()
        df['Product Price'] = df['Product Price'].apply(lambda s: s[1:])
        df.to_csv('Product.csv', index=False, encoding='utf-8')
        print(df)
