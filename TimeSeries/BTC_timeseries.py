"""
Order projection using time series

1. Download data
2. Process data
3. Train and evaluate model
4. Plot model

Data is gathered from Replica.Invoice table using ts_invoice.sql file.
"""

# =====================================================================
# 1. Download and load data (using Pandas)
# =====================================================================

import pandas as pd
import numpy as np

import matplotlib as plt
import seaborn as sns

url = "http://www.cryptodatadownload.com/cdd/gemini_BTCUSD_1hr.csv"
#url = r"C:\Users\acikgozs\Documents\Python Scripts\TimeSeries\gemini_BTCUSD_1hr.csv"

df = pd.read_csv(url, header = 1)

# =====================================================================
# 2. Process data
# =====================================================================

#del df[df.columns[0]]
#del df[df.columns[2]]
df.drop(columns = ["Unix Timestamp", "Symbol"], inplace = True)

df["Date"] = pd.to_datetime(df["Date"])

df.set_index("Date", inplace = True)

# =====================================================================
# 3. Visualize data
# =====================================================================

sns.set(rc = {"figure.figsize":(12, 5)})

sns.boxplot(x = df["Date"], data = df)

df["Open"].plot()