import os
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
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
    if WebDriverWait(browser, 10, 0.25).until(
            ec.presence_of_element_located((By.CLASS_NAME, "nav-list"))
        ):

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
                links_cat.append([cat_code, link_text, "https://www.gratis.com" + lnk.get("href")])

    return links_cat

# ==========================================================================
# Get sub category links
# ==========================================================================

def get_gratis_sub_links(browser, links_in, cl_out, il_out):
    """
    Gets sub category links from main category pages and stores them into 3rd input list with category codes
    links is a list(nx3) that generated by get_gratis_main_links and contains link address in the last column

    At each end of the category tree, it collects item info and stores them last input list
    """

    for lnk in links_in:
        browser.get(lnk[2])
        if WebDriverWait(browser, 10, 0.25).until(
            ec.presence_of_element_located((By.CLASS_NAME, "content"))
        ):

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
                        links_sub.append([cat_code, link_text, "https://www.gratis.com" + slnk.get("href")])
                        cl_out.append([cat_code, link_text, "https://www.gratis.com" + slnk.get("href")])
            
                # Retrieving minor sub categories
                get_gratis_sub_links(browser, links_sub, cl_out, il_out)

            else:
                # While loop - unless next page link is disabled
                while True:
                    # Get items
                    items_page = BeautifulSoup(browser.page_source, "html.parser")
                    items_data = items_page.find_all("div", {"class":"g-product-cards"})
                    
                    # Item links
                    for ii in items_data:
                        items_info = ii.find("div", {"class":"infos"})
                        il_out.append([lnk[0], items_info.find("a").text.strip(), "https://www.gratis.com" + items_info.find("a")["href"]])

                    if items_page.find_all("a", {"class":"nav-btns next disabled"}):
                        break

                    # There is an overlaying element which causes click error
                    # Javascript directly clicks the element itself
                    nextPageElement = browser.find_element_by_class_name("nav-btns.next")
                    browser.execute_script("arguments[0].click();", nextPageElement)

                    # Check page load status
                    WebDriverWait(browser, 10, 0.25).until(
                        ec.presence_of_element_located((By.CLASS_NAME, "col-md-4.col-sm-4.col-xs-6.product-card-wrapper"))
                    )

# ==========================================================================
# Get item details
# ==========================================================================

def get_gratis_item_details(browser, item_list):
    """
    Gets detailed item prices from item page
    """

    item_details = []
    items = []
    missing_items = []
    
    for lnk in item_list:
        browser.get(lnk[2])

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
            def_long = item_page.find("div", {"data-bind":"html: product().longDescription"}).text
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

            # Stickers
            stickers = []
            all_stickers = item_stickers.find_all("img", {"class":"product-sticker"})
            for st in all_stickers:
                try:
                    stickers.append(st["src"])
                except:
                    pass

            # Sold together with
            sold_with = item_page.find("div", {"id":"carousel-id-wi300120"})
            sw_links = sold_with.find_all("a", {"class":"search-product-link"})

            sw_items = []

            for sw in sw_links:
                sw_items.append(sw["href"][sw["href"].find("=") + 1:])

            # Related products
            rel_items = item_page.find("div", {"id":"carousel-id-wi300119"})
            ri_links = rel_items.find_all("a", {"class":"search-product-link"})

            ri_items = []

            for ri in ri_links:
                ri_items.append(ri["href"][ri["href"].find("=") + 1:])

            # category, brand, brandlink, 
            # id, name, link, 
            # originalprice, salesprice, 
            # loyaltyprice, 
            # colors, ooscolors, 
            # longdefinition, definitionname, definition, 
            # recommendations, votes, avgrating, 
            # promotions, campaigns, stickercampaign, 
            # soldwith, relateditems
            items.append([lnk[0], item_details.find("a", {"class":"manufacturer"}).text, "https://www.gratis.com" + item_details.find("a", {"class":"manufacturer"})["href"],
                item_defs.find("td", {"data-bind":"text: value"}).text, item_details.h1.text, lnk[2],
                o_price, item_price.find("span", {"class":"gr-price__amount"}).text + item_price.find("span", {"class":"gr-price__fractional"}).text.replace(",", ".").strip(),
                l_price,
                color, oos_color,
                def_long, def_name, def_value,
                review_counts[:review_counts.find(" ")], review_counts[review_counts.find("(") + 1 : review_counts.find(")")], ratings,
                promos, campaigns, stickers,
                sw_items, ri_items])

        else:
            missing_items.append(lnk[2])

    return items

# ==========================================================================
# Driver initiation
# ==========================================================================

def get_driver():
    # Initialize options
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    
    # Initialize driver
    wd_path = os.path.dirname(os.getcwd()) + r"\SeleniumChrome\chromedriver.exe"
    driver = webdriver.Chrome(wd_path, chrome_options = options)
    
    return driver

# ==========================================================================
# Execution
# ==========================================================================

browser = get_driver()
# Remove after tests, headless browser improves performance
browser.maximize_window()

url = "https://www.gratis.com"
main_links = get_gratis_main_links(browser, url)

category_links = []
item_links = []
get_gratis_sub_links(browser, main_links, category_links, item_links)

items = get_gratis_item_details(browser, item_links)

links_all = []

# item_details = pd.DataFrame(items, columns = [
#     "category", "brand", "brandlink", "id", "name", "link", 
#     "originalprice", "salesprice", "loyaltyprice", 
#     "colors", "ooscolors", 
#     "definitionname", "definition", 
#     "recommendations", "votes", "avgrating", 
#     "promotions", "campaigns", "stickercampaign", 
#     "soldwith", "relateditems"])

browser.quit()