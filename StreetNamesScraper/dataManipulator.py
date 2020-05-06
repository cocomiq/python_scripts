import pandas as pd

df = pd.read_csv(r"C:\Users\acikgozs\Documents\total_streets.csv")

df.drop("record", axis = 1, inplace = True)
df.drop_duplicates(inplace = True)
df.columns = ["city", "district", "town", "street"]

# ==========================================================================
# Cities with codes
# ==========================================================================
city_codes = [1,2,3,4,68,5,6,7,75,8,9,10,74,72,69,11,12,13,14,15,16,17,18,19,20,21,81,22,23,24,25,26,27,28,29,30,31,76,32,34,35,46,78,70,36,37,38,71,39,40,79,41,42,43,44,45,47,33,48,49,50,51,52,80,53,54,55,56,57,58,63,73,59,60,61,62,64,65,77,66,67]

cities = pd.DataFrame(df["city"].unique(), city_codes)
cities = cities.reset_index()
cities.columns = ["city_code", "city_name"]

# Data check
cities[cities['city_name'] == "TEKİRDAĞ"]

cities.index.drop()
cities.to_csv("cities.csv", index = False)

# ==========================================================================
# Districts with codes
# ==========================================================================
dist = df[["city", "district"]]
dist.drop_duplicates(inplace = True)
dist.reset_index()

dist["district_code"] = dist.groupby("city").cumcount() + 1
dist = dist.merge(cities, left_on='city', right_on='city_name')
dist.drop("city", axis = 1, inplace = True)

dist = dist[["city_code", "district_code", "city_name", "district"]]
dist.to_csv("districts.csv", index = False)


# ==========================================================================
# Towns with codes
# ==========================================================================

towns = df[["city", "district", "town"]]
towns.drop_duplicates(inplace = True)
towns["town_code"] = towns.groupby(["city", "district", "town"]).cumcount() + 1

towns = towns.merge(dist, left_on = ["city", "district"], right_on = ["city_name", "district"])
towns.drop("city_name", axis = 1, inplace = True)

towns = towns[["city_code", "district_code", "town_code", "city", "district", "town"]]
towns.to_csv("towns.csv", index = False)