import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

# ==========================================================================
# Getting Items and prices
# ==========================================================================

url = "https://www.gratis.com/"
wd_path = os.getcwd() + r"\SeleniumChrome\chromedriver.exe"

browser = webdriver.Chrome(wd_path)
browser.get(url)

soup = BeautifulSoup(browser.page_source, "html.parser")
link_data = soup.find_all("ul", {"class":"nav-list"})
links_raw = link_data[0].find_all("a")

links = []

for lnk in links_raw:
    links.append([lnk.get("href"), lnk.text])

# links icinde loopa gir
# linke tikla
# icinden urunleri al