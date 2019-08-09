import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

# ==========================================================================
# Getting links
# ==========================================================================

url = "https://www.gratis.com/"
wd_path = os.getcwd() + r"\SeleniumChrome\chromedriver.exe"

browser = webdriver.Chrome(wd_path)
browser.get(url)
time.sleep(1.5)

soup = BeautifulSoup(browser.page_source, "html.parser")
link_data = soup.find_all("ul", {"class":"nav-list"})
links_raw = link_data[0].find_all("a")

link_data[0].find

all_links = []

for lnk in links_raw:
    all_links.append([lnk.get("href"), lnk.text])

# Update all_links and add category codes
for mnp in all_links:
    # Category code insert
    cat_code = mnp[0][mnp[0].rfind("/") + 1:]
    if cat_code.isdigit():
        mnp.append(cat_code)
        mnp.append(cat_code[0:3])# Main category
        if len(cat_code) > 3:
            for i in range(3, len(cat_code), 2):
                mnp.append(cat_code[i:i + 2])#Sub categories
    
    # Replacing empty names with text in link
    if mnp[1] == "  ":
        mnp[1] = mnp[0][1:mnp[0].find("/", 2)]
    
    mnp[0] = "https://www.gratis.com" + mnp[0]

#categories
#links_raw_c = link_data[0].find_all("a", {"class":"mm-head-navs skin", "class":"mm-head-navs wo-icon"})
#subcategories
#links_raw_sc = link_data[0].find_all("a", {"class":"mm-navs", "class":"mm-navs wo-icon"})

cat_link = []


# ==========================================================================
# Getting items and pricing
# ==========================================================================

# links icinde loopa gir
for lnk in all_links[0]:
    browser.get(lnk[0])
    time.sleep(1.5)

    # alt kategorileri al ve onlardan urun getir
    soup = BeautifulSoup(browser.page_source, "html.parser")

# linke tikla
# icinden urunleri al
#browser.quit()