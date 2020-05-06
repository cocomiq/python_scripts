import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

# ==========================================================================
# Browser Initiation
# ==========================================================================
wd_path = os.path.dirname(os.getcwd()) + r"\SeleniumChrome\chromedriver.exe"
browser = webdriver.Chrome(wd_path)
browser.maximize_window()

url = "https://adres.nvi.gov.tr/VatandasIslemleri/AdresSorgu"
browser.get(url)

# ==========================================================================
# City Scaper
# ==========================================================================
soup = BeautifulSoup(browser.page_source, "html.parser")

city_data = soup.find("select", {"id":"ilListesi"})
city_names = city_data.find_all("option")
cities = [c.text for c in city_names]

# ==========================================================================
# District Scaper
# ==========================================================================

# City Selection
webdriver.support.ui.Select(browser.find_element_by_id("ilListesi")).select_by_visible_text(cities[1])

soup = BeautifulSoup(browser.page_source, "html.parser")
district_data = soup.find("select", {"id":"ilceListesi"})
district_names = district_data.find_all("option")
districts = [d.text for d in district_names]

# ==========================================================================
# Town Scaper
# ==========================================================================

# District Selection
webdriver.support.ui.Select(browser.find_element_by_id("ilceListesi")).select_by_visible_text(districts[1])

soup = BeautifulSoup(browser.page_source, "html.parser")
town_data = soup.find("select", {"id":"mahalleKoyBaglisiListesi"})
town_names = town_data.find_all("option")
towns = [t.text for t in town_names]

# ==========================================================================
# Street Scaper
# ==========================================================================

# Town Selection
webdriver.support.ui.Select(browser.find_element_by_id("mahalleKoyBaglisiListesi")).select_by_visible_text(towns[1])

soup = BeautifulSoup(browser.page_source, "html.parser")
street_data = soup.find("select", {"id":"yolListesi"})
street_names = street_data.find_all("option")
streets = [s.text for s in street_names]

# ==========================================================================
# Door Number Scaper
# ==========================================================================

# Street Selection
webdriver.support.ui.Select(browser.find_element_by_id("yolListesi")).select_by_visible_text(streets[1])

soup = BeautifulSoup(browser.page_source, "html.parser")
door_data = soup.find("select", {"id":"binaListesi"})
door_names = door_data.find_all("option")
doors = [d.text for d in door_names]

# ==========================================================================
# Internal Door Number Scaper
# ==========================================================================

# Door Selection
webdriver.support.ui.Select(browser.find_element_by_id("binaListesi")).select_by_visible_text(doors[1])

soup = BeautifulSoup(browser.page_source, "html.parser")
indoor_data = soup.find("select", {"id":"bagimsizBolumListesi"})
indoor_names = indoor_data.find_all("option")
indoors = [i.text for i in indoor_names]

# ==========================================================================
# Scraper without building number
# ==========================================================================

soup = BeautifulSoup(browser.page_source, "html.parser")

city_data = soup.find("select", {"id":"ilListesi"})
city_names = city_data.find_all("option")
cities = [c.text for c in city_names]

full_address = []
detailed_address = []

for city in cities:
    if city != "":
        # City select
        if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
            browser.find_element_by_id("adres-panel").click()
        
        webdriver.support.ui.Select(browser.find_element_by_id("ilListesi")).select_by_visible_text(city)

        # Source refresh and get districts
        WebDriverWait(browser, 3, 0.25).until(Ec.element_to_be_clickable((By.ID, "ilceListesi")))
        district_data = BeautifulSoup(browser.page_source, "html.parser").find("select", {"id":"ilceListesi"})
        district_names = district_data.find_all("option")
        districts = [d.text for d in district_names]

        for dist in districts:
            if dist != "":
                # District Selection
                if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                    browser.find_element_by_id("adres-panel").click()
                
                webdriver.support.ui.Select(browser.find_element_by_id("ilceListesi")).select_by_visible_text(dist)

                WebDriverWait(browser, 3, 0.25).until(Ec.element_to_be_clickable((By.ID, "mahalleKoyBaglisiListesi")))
                town_data = BeautifulSoup(browser.page_source, "html.parser").find("select", {"id":"mahalleKoyBaglisiListesi"})
                town_names = town_data.find_all("option")
                towns = [t.text for t in town_names]

                for town in towns:
                    if town != "":
                        # Town Selection
                        if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                            browser.find_element_by_id("adres-panel").click()
                        
                        try:
                            webdriver.support.ui.Select(browser.find_element_by_id("mahalleKoyBaglisiListesi")).select_by_visible_text(town)
                        
                        except:
                            if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                                browser.find_element_by_id("adres-panel").click()
                            
                            webdriver.support.ui.Select(browser.find_element_by_id("mahalleKoyBaglisiListesi")).select_by_visible_text(town)

                        # Source refresh and get towns
                        try: 
                            if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                                browser.find_element_by_id("adres-panel").click()
                            
                            WebDriverWait(browser, 3, 0.25).until(Ec.element_to_be_clickable((By.ID, "yolListesi")))
                            street_data = BeautifulSoup(browser.page_source, "html.parser").find("select", {"id":"yolListesi"})
                            street_names = street_data.find_all("option")
                            streets = [s.text for s in street_names]

                            for st in streets:
                                if st != "":
                                    # Street Selection
                                    if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                                        browser.find_element_by_id("adres-panel").click()

                                    # Source refresh and get streets
                                    full_address.append([city, dist, town, st])
                        
                        except:
                            full_address.append([city, dist, town, "N/A"])

# ==========================================================================
# Saving Data
# ==========================================================================
full_address[-1]
detailed_address

pd.DataFrame(full_address).to_csv("upto_end.csv")


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
# City Scaper
# ==========================================================================
def get_address(browser):
    soup = BeautifulSoup(browser.page_source, "html.parser")

    full_address = []
    detailed_address = []

    city_data = soup.find("select", {"id":"ilListesi"})
    city_names = city_data.find_all("option")
    cities = [c.text for c in city_names]

    for city in cities:
        if city != "":
            # City select
            if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                browser.find_element_by_id("adres-panel").click()
            
            webdriver.support.ui.Select(browser.find_element_by_id("ilListesi")).select_by_visible_text(city)

            # Refresh source and get districts
            WebDriverWait(browser, 3, 0.25).until(Ec.element_to_be_clickable((By.ID, "ilceListesi")))
            district_data = BeautifulSoup(browser.page_source, "html.parser").find("select", {"id":"ilceListesi"})
            district_names = district_data.find_all("option")
            districts = [d.text for d in district_names]

            for dist in districts:
                if dist != "":
                    # District Selection
                    if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                        browser.find_element_by_id("adres-panel").click()
                    
                    webdriver.support.ui.Select(browser.find_element_by_id("ilceListesi")).select_by_visible_text(dist)

                    WebDriverWait(browser, 3, 0.25).until(Ec.element_to_be_clickable((By.ID, "mahalleKoyBaglisiListesi")))
                    town_data = BeautifulSoup(browser.page_source, "html.parser").find("select", {"id":"mahalleKoyBaglisiListesi"})
                    town_names = town_data.find_all("option")
                    towns = [t.text for t in town_names]

                    for town in towns:
                        if town != "":
                            # Town Selection
                            if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                                browser.find_element_by_id("adres-panel").click()
                            
                            webdriver.support.ui.Select(browser.find_element_by_id("mahalleKoyBaglisiListesi")).select_by_visible_text(town)

                            # Refresh source and get towns
                            try: 
                                if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                                    browser.find_element_by_id("adres-panel").click()
                                
                                WebDriverWait(browser, 3, 0.25).until(Ec.element_to_be_clickable((By.ID, "yolListesi")))
                                street_data = BeautifulSoup(browser.page_source, "html.parser").find("select", {"id":"yolListesi"})
                                street_names = street_data.find_all("option")
                                streets = [s.text for s in street_names]

                                for st in streets:
                                    if st != "":
                                        # Street Selection
                                        if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                                            browser.find_element_by_id("adres-panel").click()

                                        webdriver.support.ui.Select(browser.find_element_by_id("yolListesi")).select_by_visible_text(st)

                                        # Refresh source and get streets
                                        try:
                                            if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                                                browser.find_element_by_id("adres-panel").click()
                                            
                                            WebDriverWait(browser, 3, 0.25).until(Ec.element_to_be_clickable((By.ID, "binaListesi")))
                                            door_data = BeautifulSoup(browser.page_source, "html.parser").find("select", {"id":"binaListesi"})
                                            door_names = door_data.find_all("option")
                                            doors = [d.text for d in door_names]

                                            for d in doors:
                                                if d != "":
                                                    # Door Selection
                                                    if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                                                        browser.find_element_by_id("adres-panel").click()

                                                    webdriver.support.ui.Select(browser.find_element_by_id("binaListesi")).select_by_visible_text(d)

                                                    # Refresh source and get indoor details
                                                    try:
                                                        if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                                                            browser.find_element_by_id("adres-panel").click()

                                                        WebDriverWait(browser, 3, 0.25).until(Ec.element_to_be_clickable((By.ID, "bagimsizBolumListesi")))
                                                        indoor_data = BeautifulSoup(browser.page_source, "html.parser").find("select", {"id":"bagimsizBolumListesi"})
                                                        indoor_names = indoor_data.find_all("option")
                                                        indoors = [i.text for i in indoor_names]

                                                        for ind in indoors:
                                                            if ind != "":
                                                                # Indoor Selection
                                                                if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                                                                    browser.find_element_by_id("adres-panel").click()
                                                                
                                                                webdriver.support.ui.Select(browser.find_element_by_id("bagimsizBolumListesi")).select_by_visible_text(ind)

                                                                full_address.append([city, dist, town, st, d, ind])

                                                                # Building details
                                                                if not browser.find_element_by_class_name("adres-bilgisi-panel-popup-layer-content").is_displayed():
                                                                    browser.find_element_by_id("adres-bilgisi-panel").click()
                                                                
                                                                WebDriverWait(browser, 3, 0.25).until(Ec.visibility_of_element_located((By.CLASS_NAME, "adres-bilgisi-panel-popup-layer-content")))
                                                                building_info = BeautifulSoup(browser.page_source, "html.parser").find("table", {"class":"table aksHarita table-bordered table-hover ui-responsive"})
                                                                building_detail = building_info.find_all("td")

                                                                for det in building_detail:
                                                                    da.append(det.get("data-title"), det.text)

                                                                detailed_address.append(da)
                                                                
                                                                if not browser.find_element_by_class_name("adres-panel-popup-layer-content").is_displayed():
                                                                    browser.find_element_by_id("adres-bilgisi-panel").click()

                                                    except:
                                                        full_address.append([city, dist, town, st, d, "N/A"])
                                                        #detailed_address.append([])
                                        except:
                                            full_address.append([city, dist, town, st, "N/A", "N/A"])
                            except:
                                full_address.append([city, dist, town, "N/A", "N/A", "N/A"])