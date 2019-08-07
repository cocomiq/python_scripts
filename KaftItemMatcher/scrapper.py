# ==========================================================================
# Getting Item List
# ==========================================================================
import os
import datetime
import time
import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


url = "https://www.kaft.com/erkek-tisort"

urlgetter = urllib3.PoolManager() 
raw_html = urlgetter.request("GET", url)

soup = BeautifulSoup(raw_html.data, 'html.parser')
product_data = soup.find_all("a", {"class":"basicProductDisplayLink"})

products = []

for prd in product_data:
    products.append([prd.get("href"), prd.get("data-id"), prd.get("data-name"), prd.get("data-brand"), prd.get("data-variant"), prd.get("data-price"), prd.get("data-category")])

df = pd.DataFrame(products, columns = ["web_address", "id", "name", "brand", "type", "price", "category"])
df.to_json(os.getcwd() + r"\KaftItemMatcher\items.json", orient = "records")

# ==========================================================================
# Getting wishlisted items from Wardrobe
# ==========================================================================

wardrobe = pd.read_json(os.getcwd() + r"\KaftItemMatcher\wardrobe.json")

for index, row in wardrobe.iterrows():
    if np.isnan(row["wishlist"]):
        wardrobe.drop(index, inplace = True)

#wardrobe["wishlist"] = wardrobe["wishlist"].astype("int64")

# ==========================================================================
# Automatic Item Matcher
# ==========================================================================

matcher_url = "https://www.kaft.com/teemachine"
wd_path = os.getcwd() + r"\KaftItemMatcher\chromedriver.exe"

browser = webdriver.Chrome(wd_path)
browser.get(matcher_url)

# Selection Criteria -> Erkek - L - Originals - Relax - Regular
browser.find_element_by_class_name("size-image.large-men").click()
browser.find_element_by_class_name("collection-image.original").click()
browser.find_element_by_class_name("collection-image.minimal").click()
browser.find_element_by_class_name("collection-image.street").click()

result_list = []
matched = 0

start_time = datetime.datetime.now()

while matched < 3 or  (datetime.datetime.now() - start_time).seconds < 60:
    browser.find_element_by_class_name("buton").click()
    items = browser.find_elements_by_class_name("basicProductDisplay")

    item_list = []
    match_list = []

    for item in items:
        item_list.append(int(item.get_attribute("productid")))
        if wardrobe[(wardrobe["id"] == int(item.get_attribute("productid")))]["id"].size > 0:
            match_list.append(1)
        else:
            match_list.append(0)

    result_list.append(item_list + match_list + datetime.datetime.now())
    matched = sum(match_list)
    time.sleep(0.8)

print(result_list)

result_set = pd.DataFrame(result_list, columns = ["item_1", "item_2", "item_3", "matched_1", "matched_2", "matched_3", "result_date"])
#result_set.to_json(os.getcwd() + r"\KaftItemMatcher\results.json", orient = "records")

#browser.close()