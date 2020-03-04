import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split
import pickle
import matplotlib as plt

# ==========================================================================
# Load and prepare data
# ==========================================================================

df = pd.read_csv(r"C:\Users\acikgozs\Documents\active_prediction.csv", sep = ";")

df.head()
#df.drop(columns = ["CAMPAIGN", "ACCOUNT_NUMBER"], inplace = True)

df_base = df.drop(columns = ["CAMPAIGN", "ACCOUNT_NUMBER"])
df_base.dropna()
df_base = df_base[df_base["AGE"] > 0]
df_base.reset_index()

x = df_base.iloc[:,1:]
y = df_base.iloc[:,:1]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 7)

data_dmatrix = xgb.DMatrix(data = x_train, label = y_train)

# ==========================================================================
# XGBoost Model
# ==========================================================================

xgb_reg = xgb.XGBRegressor(objective = "binary:logistic")

eval_set = [(x_train, y_train), (x_test, y_test)]
eval_metric = ["auc","error"]

#%time xgb_reg.fit(X_train, y_train, eval_metric = eval_metric, eval_set = eval_set, verbose = True)

xgb_reg.load_model("active_xgb_save.model")
#xgb_reg = pickle.load(open("active.model", 'rb'))
#xgb_reg.fit(x_train, y_train)

preds = xgb_reg.predict(x_test)

# ==========================================================================
# Accuracy
# ==========================================================================

predictions = [round(value) for value in preds]

accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

pd.DataFrame(preds.round())

#y_test

# ==========================================================================
# Saving model
# ==========================================================================

#pickle.dump(xgb_reg, open("active.model", "wb"))
xgb_reg.save_model("active_xgb_save.model")

# ==========================================================================
# Charts
# ==========================================================================

xgb.plot_tree(xgb_reg, num_trees = 0)
plt.rcParams['figure.figsize'] = [50, 10]

xgb.plot_importance(xgb_reg)
plt.rcParams['figure.figsize'] = [5, 5]

# ==========================================================================
# Single campaign results
# ==========================================================================

dfp = pd.read_csv(r"C:\Users\acikgozs\Documents\active_prediction202002.csv", sep = ";")

dfp.head()

dfp.dropna()
dfp = dfp[dfp["AGE"] > 0]
dfp.reset_index()

x = dfp.iloc[:,3:]
#y = dfp.iloc[:,2:3]

preds = xgb_reg.predict(x)

pd.DataFrame(preds, dfp["ACCOUNT_NUMBER"]).to_csv("2020C3_pred.csv")