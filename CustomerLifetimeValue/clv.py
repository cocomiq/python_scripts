import pandas as pd
import matplotlib as plt

from lifetimes import plotting
from lifetimes import utils
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter

from sklearn.model_selection import train_test_split

# ==========================================================================
# Load and prepare data
# ==========================================================================
path = r"C:\Users\acikgozs\Documents\CLV_1.csv"

df = pd.read_csv(path, sep = ";", header = 0)
df.head()

# removal of test records and negative value
df.drop(df[df["RECENCY"] > df["T"]].index, inplace = True)
#df.drop(df[df["MONETARY_VALUE"] <= 10.00].index, inplace = True)

# ==========================================================================
# Data check
# ==========================================================================
# Order distribution by frequency
df["FREQUENCY"].plot(kind = "hist", bins = 50)

# ==========================================================================
# BG/NBD model
# ==========================================================================

bgf = BetaGeoFitter(penalizer_coef = 0.01)
bgf.fit(df["FREQUENCY"], df["RECENCY"], df["T"])

bgf.summary

plotting.plot_frequency_recency_matrix(bgf)
plotting.plot_probability_alive_matrix(bgf)

# Repeat transaction model check
plotting.plot_period_transactions(bgf)

# ==========================================================================
# Ranking reps from best to worst
# ==========================================================================

t = 1
df["predicted_purchases"] = bgf.conditional_expected_number_of_purchases_up_to_time(t, df["FREQUENCY"], df["RECENCY"], df["T"])
df.sort_values(by = "predicted_purchases").tail(10)

# ==========================================================================
# Gamma Gamme Model
# Model assumes that there is no relationship between the monetary value and the purchase frequency
# ==========================================================================

df[["MONETARY_VALUE", "FREQUENCY"]].corr()

ggf = GammaGammaFitter(penalizer_coef = 0)
ggf.fit(df["FREQUENCY"], df["MONETARY_VALUE"])

ggf.conditional_expected_average_profit(df["FREQUENCY"], df["MONETARY_VALUE"]).head(10)

print("Expected conditional average profit: %s, Average profit: %s" % (
    ggf.conditional_expected_average_profit(
        df["FREQUENCY"],
        df["MONETARY_VALUE"]
    ).mean(), 
    df[df["FREQUENCY"] > 0]["MONETARY_VALUE"].mean()))


bgf.fit(df["FREQUENCY"], df["RECENCY"], df["T"])

pred = ggf.customer_lifetime_value(
    bgf, #the model to use to predict the number of future transactions
    df["FREQUENCY"],
    df["RECENCY"],
    df["T"],
    df["MONETARY_VALUE"],
    time = 1, # year
    discount_rate = 0.02 # campaignly discount rate ~ 20% annually
)

pred.head(10)
pred.tail(10)
pred.mean()
pred.median()

df["MONETARY_VALUE"].mean()
df["T"].mean()

df[df["T"] < 14]["T"].count()
df[df["T"] > 13]["T"].count()