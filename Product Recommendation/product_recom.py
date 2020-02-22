import pandas as pd
import numpy as np
import surprise as sp

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate

# ==========================================================================
# Load and prepare data
# ==========================================================================

path = r"C:\Users\acikgozs\Documents\invoice_rep_item.csv"

df = pd.read_csv(path, sep = ";", header = 0)
#df.drop(df[df["TOTAL_QUANTITY"] > 30].index, inplace = True)
#df.head()

# Value normalization
df_matrix = df.pivot(index = "ITEM_CODE", columns = "ACCOUNTNUM", values = "TOTAL_QUANTITY")
df_matrix_norm = round((df_matrix - 1)/(df_matrix.max() - 1), 4)

# Dataframe transpose and create row based data
ddf = df_matrix_norm.T
ddf.reset_index(inplace = True)
data_norm = pd.melt(ddf, id_vars = ["ACCOUNTNUM"], value_name = "TOTAL_QUANTITY").dropna()

# Dataset creation for model
rdr = sp.Reader(rating_scale = (0, 1))
ds = sp.Dataset.load_from_df(data_norm, rdr)

# ==========================================================================
# Model selection and feature tuning
# ==========================================================================

param_grid = {
        "n_epochs": [5, 10],
        "lr_all": [0.002, 0.005],
        "reg_all": [0.4, 0.6]
    }

gs = sp.model_selection.GridSearchCV(sp.SVD, param_grid, measures = ["rmse", "mae"], cv = 3)
gs.fit(ds)

gs.best_params
gs.best_score

# Manual model selection and cv
algo = sp.SVD()
sp.model_selection.cross_validate(algo, ds, measures = ["RMSE", "MAE"], cv = 5, verbose=True)

# ==========================================================================
# Model train
# ==========================================================================

train_set, test_set = sp.model_selection.train_test_split(ds, test_size = 0.3)
algo.fit(train_set)
predictions = algo.test(test_set)

sp.accuracy.rmse(predictions)
df_p = pd.DataFrame(predictions, columns=['uid', 'iid', 'rui', 'est', 'details'])

# ==========================================================================
# Model fit
# ==========================================================================

trainset = ds.build_full_trainset()
algo.fit(trainset)

# Sigle record check
algo.predict(12104957, "1313366", r_ui = 0, verbose = True)

# ==========================================================================
# Incentive items
# ==========================================================================

#unique_items = data_norm.ITEM_CODE.unique()
unique_reps = data_norm.ACCOUNTNUM.unique()
check_items = ["9099800", "1144000", "3567400", "5868800", "2055300", "1299062", "1432900", "1302857", "9475100", "5148300"]

#unique_items = pd.DataFrame(unique_items)
unique_reps = pd.DataFrame(unique_reps)
check_items = pd.DataFrame(check_items)

# Adding key column to cross join tables
#unique_items["key"] = 0
unique_reps["key"] = 0
check_items["key"] = 0

overall = unique_reps.merge(check_items, on = "key", how = "outer")
overall.drop("key", axis = 1, inplace = True)
overall["base"] = 0
overall.columns = ["account", "item", "base"]

# New dataset for selected incentive items
overall_ds = sp.Dataset.load_from_df(overall, rdr)

# Create a test split and asign all values to test
# !!!!!Need to check how to convert df to tuple list!!!!!
ptrain, ptest = sp.model_selection.train_test_split(overall_ds, test_size = 1.0)

preds = algo.test(ptest)
pred = pd.DataFrame(preds)
pr = pred.pivot(index = "uid", columns = "iid", values = "est")
pr.to_csv(r"C:\Users\acikgozs\Documents\predictions.csv")