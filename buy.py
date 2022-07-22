import os
from time import sleep
from selenium import webdriver
import pandas as pd

class Buy(webdriver.Chrome):
    def __init__(self,driver_path="D:\Projects",teardown=False):
        self.driver_path=driver_path
        self.teardown=teardown
        os.environ['PATH']+=self.driver_path
        super(Buy, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def visit_home_page(self):
        self.get("https://www.amazon.in/")

    def search_item_you_want(self,item_you_want):
        search_field=self.find_element_by_id('twotabsearchtextbox')
        search_field.clear()
        search_field.send_keys(item_you_want)
        self.implicitly_wait(10)

    def click_search(self):
        search_button=self.find_element_by_id('nav-search-submit-text')
        search_button.click()

        self.implicitly_wait(10)
    def pull_data_to_store_in_csv(self):
        product_name = []
        product_price = []
        product_reviews = []
        name=self.find_elements_by_xpath("//span[@class='a-size-medium a-color-base a-text-normal']")
        for n in name:
            product_name.append(n.text)
        price=self.find_elements_by_xpath("//span[@class='a-price']")
        for pr in price:
            product_price.append(pr.text)
        number_of_reviews=self.find_elements_by_xpath("//div[@class='a-row a-size-small']")
        for rev in number_of_reviews:
            product_reviews.append(rev.text)
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
        data={'Product Name':product_name,'Product Price':product_price,'Total Reviews':product_reviews}
        df = pd.DataFrame.from_dict(data,orient='index')
        df=df.transpose()
        df.to_csv('Product.csv',index=False,encoding='utf-8')
        print(df)



