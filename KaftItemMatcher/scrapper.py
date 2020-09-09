import os
import datetime
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# ==========================================================================
# Getting Item List
# ==========================================================================
def kaft_item_scraper(browser):
    url = "https://www.kaft.com/erkek-tisort"
    browser.get(url)

    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < 2:
        browser.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
    
    # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(browser, 10, 1).until(
            ec.presence_of_element_located((By.CLASS_NAME, "primaryImage"))
        )

    soup = BeautifulSoup(browser.page_source, "html.parser")
    product_data = soup.find_all("a", {"class":"basicProductDisplayLink"})

    products = []

    for prd in product_data:
        products.append([prd.get("href"), prd.get("data-id"), prd.get("data-name"), prd.get("data-brand"), prd.get("data-variant"), prd.get("data-price"), prd.get("data-category"), prd.find("img").get("src")[:prd.find("img").get("src").find("?")]])

    df = pd.DataFrame(products, columns = ["web_address", "id", "name", "brand", "type", "price", "category", "img_address"])
    df.to_json(os.path.dirname(os.getcwd()) + r"\KaftItemMatcher\items.json", orient = "records")

    wardrope = df[["id", "name", "web_address"]]
    wardrope["isbought"] = np.nan
    wardrope["wishlist"] = np.nan
    wardrope.to_json(os.path.dirname(os.getcwd()) + r"\KaftItemMatcher\wardrobe.json", orient = "records")

# ==========================================================================
# Automatic Item Matcher
# ==========================================================================
def kaft_item_matcher(browser):
    matcher_url = "https://www.kaft.com/teemachine"
    browser.get(matcher_url)

    # Selection Criteria -> Erkek - L - Originals - Relax - Regular
    browser.find_element_by_class_name("size-image.medium-men").click()
    # Clicked by default
    #browser.find_element_by_class_name("collection-image.street").click()

    wardrobe = pd.read_json(os.path.dirname(os.getcwd()) + r"\KaftItemMatcher\wardrobe.json")

    for index, row in wardrobe.iterrows():
        if np.isnan(row["wishlist"]):
            wardrobe.drop(index, inplace = True)

    result_list = []
    matched = 0

    start_time = datetime.datetime.now()

    while matched < 3 and (datetime.datetime.now() - start_time).seconds < 30:
        browser.find_element_by_class_name("buton").click()
        time.sleep(round(np.random.rand() + 0.6, 2))
        items = browser.find_elements_by_class_name("basicProductDisplay")

        item_list = []
        match_list = []

        for item in items:
            item_list.append(int(item.get_attribute("productid")))
            if wardrobe[(wardrobe["id"] == int(item.get_attribute("productid")))]["id"].size > 0:
                match_list.append(1)
            else:
                match_list.append(0)

        result_list.append(item_list + match_list)
        matched = sum(match_list)

    
    result_set = pd.DataFrame(result_list, columns = ["item_1", "item_2", "item_3", "matched_1", "matched_2", "matched_3", "result_date"])
    #result_set.to_json(os.getcwd() + r"\KaftItemMatcher\results.json", orient = "records")

    result_set

# ==========================================================================
# Main Run
# ==========================================================================
wd_path = os.path.dirname(os.getcwd()) + r"\SeleniumChrome\chromedriver.exe"
browser = webdriver.Chrome(wd_path)
browser.maximize_window()

# kaft_item_scraper(browser)
kaft_item_matcher(browser)

browser.close()