import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import pandas as pd

# ==========================================================================
# Getting main menu links
# ==========================================================================

wd_path = os.getcwd() + r"\SeleniumChrome\chromedriver.exe"
browser = webdriver.Chrome(wd_path)
browser.maximize_window()
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


# OLD CODE ##################################

url = "https://www.gratis.com/maskara/kategori/5010101"

browser.get(url)
time.sleep(2)

links_items = []

brands_page = BeautifulSoup(browser.page_source, "html.parser")
brands_data = brands_page.find_all("div", {"class":"list-filter-cards active"})

for brd in brands_data:
    if brd.div.span.text == "Markalar":
        brands = brd.find_all("div", {"class":"form-group checkbox-structure"})


url = "https://www.gratis.com/maskara/kategori/5010101"

browser.get(url)
time.sleep(2)

links_items = []

# While loop - unless next page link is disabled
#go_next = True
while True:
    # Get items
    items_page = BeautifulSoup(browser.page_source, "html.parser")
    items_data = items_page.find_all("div", {"class":"g-product-cards"})
    
    # Item links
    for ii in items_data:
        items_info = ii.find("div", {"class":"infos"})
        #category code, name, link
        #url_list[2], items_info.find("a").text.strip(), "https://www.gratis.com" + items_info.find("a")["href"]
        links_items.append([items_info.find("a").text.strip(), "https://www.gratis.com" + items_info.find("a")["href"]])

    if items_page.find_all("a", {"class":"nav-btns next disabled"}):
        #go_next = False
        break
    #else:
        #browser.find_element_by_class_name("nav-btns next").click()
        #time.sleep(2)
    
    # Go to next page
    browser.find_element_by_class_name("nav-btns.next").click()
    time.sleep(2)

links_items




#url = "https://www.gratis.com/loreal-paris-unlimited-maskara/urun/Lorealparis1068?sku=10127816"
url = "https://www.gratis.com/benri-disk-pamuk-140-adet/urun/10042263?sku=10042263"

item_details = []

browser.get(url)

if WebDriverWait(browser, 10, 0.25).until(
        ec.presence_of_element_located((By.CLASS_NAME, "col-md-7.col-sm-7.col-xs-12"))
    ):
    item_page = BeautifulSoup(browser.page_source, "html.parser")
    item_details = item_page.find("div", {"class":"col-md-7 col-sm-7 col-xs-12"})
    item_stickers = item_page.find("div", {"id":"image-viewer"})
    item_defs = item_page.find("table", {"class":"specs-table"})
    item_price =  item_details.find("g-price", {"class":"pdp-price pdp-price-main"})

    # Original price check
    org_price = item_details.find("span", {"class":"gr-price pdp-price gr-price_greyed gr-price_crossed"})
    if org_price:
        o_price = org_price.find("span", {"class":"gr-price__amount"}).text + org_price.find("span", {"class":"gr-price__fractional"}).text.replace(",", ".").strip()
    else:
        o_price = -1

    # Loyalty price check
    loyalty_price =  item_details.find("span", {"class":"gr-price loyalty-price"})
    if loyalty_price:
        l_price = loyalty_price.find("span", {"class":"gr-price__amount"}).text + loyalty_price.find("span", {"class":"gr-price__fractional"}).text.replace(",", ".").strip()
    else:
        l_price = -1

    # Colors
    try:
        browser.find_element_by_class_name("color-toggle").click()
    except:
        pass

    oos_color = []
    color = []

    item_colors = item_details.find_all("a", {"class":"gratis-color"})
    for ic in item_colors:
        if ic["class"] == ["gratis-color", "no-stock"]:
            oos_color.append(ic["data-color"])
        else:
            color.append(ic["data-color"])

    # Definitions
    item_page.find("div", {"data-bind":"html: product().longDescription"}).text
    def_attr = item_defs.find_all("tr")

    def_name = []
    def_value = []
    for da in def_attr:
        def_name.append(da.find("td", {"data-bind":"text: name"}).text)
        def_value.append(da.find("td", {"data-bind":"text: value"}).text)

    # Review info if exists
    review_info = item_page.find("div", {"class":"bv-percent-recommend-container"})
    if review_info:
        review_counts = review_info.text.strip()
        review_grades = item_page.find_all("span", {"class":"bv-secondary-rating-summary-rating"})
    else:
        review_counts = ""
        review_grades = []
    
    # Recommends
    review_counts[:review_counts.find(" ")]
    # Votes
    review_counts[review_counts.find("(") + 1 : review_counts.find(")")]
    # Avg rating
    # General, quality, value
    ratings = []
    for rg in review_grades:
        ratings.append(rg.text.strip())

    # Promotions
    item_promos = item_page.find_all("img", {"alt":"Promo sticker"})
    promo_def = item_page.find("div", {"class":"campaign-card"})

    promos = []

    for ip in item_promos:
        promos.append(ip["src"])
    
    if promo_def:
        campaigns = promo_def.text
    else:
        campaigns = ""

    # Sold together with
    sold_with = item_page.find("div", {"id":"carousel-id-wi300120"})
    sw_links = sold_with.find_all("a", {"class":"search-product-link"})

    sw_items = []

    for sw in sw_links:
        sw_items.append(sw["href"][sw["href"].find("=")+1:])

    # Related products
    rel_items = item_page.find("div", {"id":"carousel-id-wi300119"})
    ri_links = rel_items.find_all("a", {"class":"search-product-link"})

    ri_items = []

    for ri in ri_links:
        ri_items.append(ri["href"][ri["href"].find("=")+1:])

    # Category
    #item_list[0]
    # Brand
    item_details.find("a", {"class":"manufacturer"}).text
    # Brand link
    "https://www.gratis.com" + item_details.find("a", {"class":"manufacturer"})["href"]
    # ID
    item_defs.find("td", {"data-bind":"text: value"}).text
    # Name
    item_details.h1.text
    # Link
    url
    # Original price if exists
    o_price
    # Sales price
    item_price.find("span", {"class":"gr-price__amount"}).text + item_price.find("span", {"class":"gr-price__fractional"}).text.replace(",", ".").strip()
    # Loyalty price if exists
    l_price
    # Colors
    color
    oos_color
    # Definitions
    def_name
    def_value
    # Recommends
    review_counts[:review_counts.find(" ")]
    # Votes
    review_counts[review_counts.find("(") + 1 : review_counts.find(")")]
    # Avg Rating
    ratings
    # Promotions
    promos
    campaigns
    # Stickers
    item_stickers.find("img", {"class":"product-sticker product-sticker_top-right"})["src"]
    # Sold together with items
    sw_items
    # Related items
    ri_items