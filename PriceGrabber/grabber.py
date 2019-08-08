import urllib3
from bs4 import BeautifulSoup

# ==========================================================================
# Getting Items and prices
# ==========================================================================

url = "https://www.gratis.com/"

urlgetter = urllib3.PoolManager() 
raw_html = urlgetter.request("GET", url)

soup = BeautifulSoup(raw_html.data, 'html.parser')
product_data = soup.find_all("ul", {"class":"mm-list"})

products = []

