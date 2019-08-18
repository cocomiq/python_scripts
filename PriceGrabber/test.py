import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

# ==========================================================================
# Getting main menu links
# ==========================================================================

wd_path = os.getcwd() + r"\SeleniumChrome\chromedriver.exe"
browser = webdriver.Chrome(wd_path)
url = "https://www.gratis.com"

browser.get(url)
time.sleep(2)

soup = BeautifulSoup(browser.page_source, "html.parser")
link_data = soup.find_all("ul", {"class":"nav-list"})
links_raw = link_data[0].find_all("a")

links_cat = []
#main category, parent category, category code, name, link

for lnk in links_raw:
    cat_code = lnk.get("href")[lnk.get("href").rfind("/") + 1:]
    
    if lnk.text == " ":
        link_text = lnk.get("href")[1:lnk.get("href").find("/", 2)]
    else:
        link_text = lnk.text
    
    if cat_code.isdigit() and len(cat_code) == 3:
        links_cat.append([0, 0, cat_code, link_text, "https://www.gratis.com" + lnk.get("href")])

links_all = []

for lnk in links_cat:
    browser.get("https://www.gratis.com/ruj/kategori/5010201?N=3160592764&Ns=&Nr=AND(product.active:1,NOT(sku.listPrice:0.000000))&No=0")
    time.sleep(2)

    # If show all link exists, click on to extend sub category list
    try:
        browser.find_element_by_class_name("show-all").click()
    except:
        pass
        
    sub_page = BeautifulSoup(browser.page_source, "html.parser")
    links_data = sub_page.find_all("ul", {"class":"content"})
    links_raw = links_data[0].find_all("a")

    links_sub = []

    # if condition = eger sub link varsa al, yoksa itemlari cek
    if links_raw:
        for slnk in links_raw:
            cat_code = slnk.get("href")[slnk.get("href").rfind("/") + 1:]
            
            if slnk.text == " ":
                link_text = slnk.get("href")[1:slnk.get("href").find("/", 2)]
            else:
                link_text = slnk.text.strip("\n")
            
            if cat_code.isdigit():
                links_sub.append([lnk[2], cat_code[0:len(cat_code) - 2], cat_code, link_text, "https://www.gratis.com" + slnk.get("href")])

        links_all.append(links_sub)
    # Retrieving 2x sub categories
        #get_gratis_sub_links(browser, links_sub, links_out)
    # end of if condition
    else:
        print("false")

    # filtreleri kullarak markalara gore data cekilir
    break


# BACKUP CODE ##################################
""" url = "https://www.gratis.com/"
wd_path = os.getcwd() + r"\SeleniumChrome\chromedriver.exe"

browser = webdriver.Chrome(wd_path)
browser.get(url)
time.sleep(1.5)

soup = BeautifulSoup(browser.page_source, "html.parser")
link_data = soup.find_all("ul", {"class":"nav-list"})
links_raw = link_data[0].find_all("a")

links_cat = []

for lnk in links_raw:
    cat_code = lnk.get("href")[lnk.get("href").rfind("/") + 1:]
    
    if lnk.text == " ":
        link_text = lnk.get("href")[1:lnk.get("href").find("/", 2)]
    else:
        link_text = lnk.text
    
    if cat_code.isdigit() and len(cat_code) == 3:
        links_cat.append([0, 0, cat_code, link_text, "https://www.gratis.com" + lnk.get("href")])
"""
# BACKUP CODE ##################################

# BACKUP CODE ##################################
# Update all_links and add category codes
""" for mnp in links_cat:
    # Category code insert
    cat_code = mnp[0][mnp[0].rfind("/") + 1:]
    if cat_code.isdigit():
        mnp.append(cat_code[0:3])# Main category
        mnp.append(cat_code[0:len(cat_code) - 2])# Parent category
        mnp.append(cat_code)
        if len(cat_code) > 3:
            for i in range(3, len(cat_code), 2):
                mnp.append(cat_code[i:i + 2])#Sub categories
    
    # Replacing empty names with text in link
    if mnp[1] == "  ":
        mnp[1] = mnp[0][1:mnp[0].find("/", 2)]
    
    mnp[0] = "https://www.gratis.com" + mnp[0]
"""

#categories
#links_raw_c = link_data[0].find_all("a", {"class":"mm-head-navs skin", "class":"mm-head-navs wo-icon"})
#subcategories
#links_raw_sc = link_data[0].find_all("a", {"class":"mm-navs", "class":"mm-navs wo-icon"})
# BACKUP CODE ##################################

# BACKUP CODE ##################################
"""
for lnk in links_cat:
    browser.get(lnk[4])
    time.sleep(2)

    # Sub links from main category
    sub_page = BeautifulSoup(browser.page_source, "html.parser")
    links_data = sub_page.find_all("ul", {"class":"content"})
    links_raw = links_data[0].find_all("a")

    links_sub = []
    # eger alt kategori varsa bitene kadar git kontrolu koyulmali
    for slnk in links_raw:
        # Adding sub link to all links
        cat_code = slnk.get("href")[slnk.get("href").rfind("/") + 1:]
        
        if slnk.text == " ":
            link_text = slnk.get("href")[1:slnk.get("href").find("/", 2)]
        else:
            link_text = slnk.text.strip("\n")
        
        if cat_code.isdigit():
            links_sub.append([lnk[2], cat_code[0:len(cat_code) - 2], cat_code, link_text, "https://www.gratis.com" + slnk.get("href")])

        # Retrieving items from sub link
        browser.get("https://www.gratis.com" + slnk.get("href"))
        time.sleep(2)

        # filtreleri kullarak markalara gore data cekilir
        break
    break
"""
# BACKUP CODE ##################################