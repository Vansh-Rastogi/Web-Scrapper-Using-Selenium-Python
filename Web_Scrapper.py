from buyfromamazon.buy import Buy
from time import sleep

with Buy() as buying:
    buying.visit_home_page()
    buying.search_item_you_want(input())
    buying.click_search()
    sleep(2)
    buying.pull_data_to_store_in_csv()


