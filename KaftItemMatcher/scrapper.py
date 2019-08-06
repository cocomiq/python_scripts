# ==========================================================================
# Getting Item List
# ==========================================================================

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.kaft.com/erkek-tisort"

raw_html = urlopen(url)
soup = BeautifulSoup(raw_html, 'lxml')
product_data = soup.find_all("a", {"class":"basicProductDisplayLink"})

products = []

for prd in product_data:
    products.append([prd.get("href"), prd.get("data-id"), prd.get("data-name"), prd.get("data-brand"), prd.get("data-variant"), prd.get("data-price"), prd.get("data-position"), prd.get("data-category")])

# ==========================================================================
# Data Visualization
# ==========================================================================

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

df = pd.DataFrame(products)

df.columns = ["web_address", "id", "name", "brand", "type", "price", "site_order", "category"]

df.head()