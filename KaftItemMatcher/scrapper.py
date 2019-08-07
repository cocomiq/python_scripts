# ==========================================================================
# Getting Item List
# ==========================================================================
import urllib3
from bs4 import BeautifulSoup
import os
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

wardrobe = pd.read_json(r"C:\Users\acikgozs\Documents\Python Scripts\KaftItemMatcher\wardrobe.json")

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

# Enter Details - Erkek - L - Originals - Relax - Regular
browser.find_element_by_class_name("size-image.large-men").click()
browser.find_element_by_class_name("collection-image.original").click()
browser.find_element_by_class_name("collection-image.minimal").click()
browser.find_element_by_class_name("collection-image.street").click()
browser.find_element_by_class_name("buton").click()

# Get random items and check wishlist
items = browser.find_elements_by_class_name("basicProductDisplay")

#item_list = pd.DataFrame(columns = wardrobe.columns)
item_list = []

for item in items:
    #item_list.append(wardrobe[wardrobe["id"] == item.get_attribute("productid")])
    print(item.get_attribute("productid"))
    item_list.append(item.get_attribute("productid"))
    #print(wardrobe[wardrobe["id"] == item.get_attribute("productid")])