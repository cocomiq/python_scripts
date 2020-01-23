import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split

# ==========================================================================
# Load and prepare data
# ==========================================================================

df = pd.read_csv(r"C:\Users\acikgozs\Documents\active_prediction_v1.csv", sep = ";")

df.head()
#df.drop(columns = ["CAMPAIGN", "ACCOUNT_NUMBER"], inplace = True)

df_base = df.drop(columns = ["CAMPAIGN", "ACCOUNT_NUMBER"])
df_base.dropna()
df_base = df_base[df_base["AGE"] > 0]
df_base.reset_index()

x = df_base.iloc[:,1:]
y = df_base.iloc[:,:1]

seed = 7
t_size = 0.3

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = t_size, random_state = seed)

data_dmatrix = xgb.DMatrix(data = x_train, label = y_train)

# ==========================================================================
# XGBoost Model
# ==========================================================================

xgb_reg = xgb.XGBRegressor(objective = "binary:logistic")

xgb_reg.fit(x_train, y_train)

preds = xgb_reg.predict(x_test)

# ==========================================================================
# Accuracy
# ==========================================================================

predictions = [round(value) for value in preds]

accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))


pd.DataFrame(preds.round())

y_test