import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

# ==========================================================================
# Get main menu header links
# ==========================================================================

def get_gratis_main_links(browser, url):
    """
    Gets main menu links from homepage and stores them into a list with category codes
    """
    
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

    return links_cat

# ==========================================================================
# Get sub category links
# ==========================================================================

def get_gratis_sub_links(browser, links_in):
    """
    Gets sub category links from main category pages and stores them into a list with category codes
    links is a list(nx5) that generated by get_gratis_main_links and contains link address in the last column
    """

    links_sc = []
    links_items = []

    for lnk in links_in:
        browser.get(lnk[4])
        time.sleep(2)

        # If show all link exists, click on it to extend sub category list
        try:
            browser.find_element_by_class_name("show-all").click()
        except:
            pass

        sub_page = BeautifulSoup(browser.page_source, "html.parser")
        links_data = sub_page.find_all("ul", {"class":"content"})
        links_raw = links_data[0].find_all("a")

        links_sub = []

        if links_raw:
            for slnk in links_raw:
                cat_code = slnk.get("href")[slnk.get("href").rfind("/") + 1:]
                
                if slnk.text == " ":
                    link_text = slnk.get("href")[1:slnk.get("href").find("/", 2)]
                else:
                    link_text = slnk.text.strip("\n")
                
                if cat_code.isdigit():
                    links_sub.append([cat_code[0:3], cat_code[0:len(cat_code) - 2], cat_code, link_text, "https://www.gratis.com" + slnk.get("href")])

            links_sc.append(links_sub)
        
            # Retrieving minor sub categories
            links_sc.append(get_gratis_sub_links(browser, links_sub))

        else:
            # While loop - unless next page link is disabled
            #go_next = True
            while True:
                # Get items
                items_page = BeautifulSoup(browser.page_source, "html.parser")
                items_data = items_page.find_all("div", {"class":"g-product-cards"})
                
                # Item links
                for ii in items_data:
                    items_info = ii.find("div", {"class":"infos"})
                    links_items.append([lnk[2], items_info.find("a").text.strip(), "https://www.gratis.com" + items_info.find("a")["href"]])

                if items_page.find_all("a", {"class":"nav-btns next disabled"}):
                    #go_next = False
                    break
                #else:
                    #browser.find_element_by_class_name("nav-btns next").click()
                    #time.sleep(2)
                
                # Go to next page
                browser.find_element_by_class_name("nav-btns.next").click()
                time.sleep(2)

    return links_sc, links_items

# ==========================================================================
# Get item details
# ==========================================================================

def get_gratis_item_details(browser, item_list):
    """
    Gets detailed item prices from item page
    """

    browser.get(item_list[4])
    time.sleep(2)

    item_details = []

    return False

# ==========================================================================
# Execution
# ==========================================================================

wd_path = os.getcwd() + r"\SeleniumChrome\chromedriver.exe"
browser = webdriver.Chrome(wd_path)
browser.maximize_window()
url = "https://www.gratis.com"

links_all = []

#browser.quit()