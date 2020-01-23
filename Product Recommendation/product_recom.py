import pandas as pd
import numpy as np
import surprise as sp
#from sklearn.preprocessing import MinMaxScaler

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate

path = r"C:\Users\acikgozs\Documents\invoice_rep_item.csv"

df = pd.read_csv(path, sep = ";", header = 0)
#df.drop(df[df.ITEM_CODE == "SAMPLE"].index, inplace = True)
#df.drop(df[df["TOTAL_QUANTITY"] > 30].index, inplace = True)
df.head()

#df_matrix = df.pivot(index = "ACCOUNTNUM", columns = "ITEM_CODE", values = "TOTAL_QUANTITY")
# MinMaxScaler doesn't work as expected
# It converts data into array and overwrites row/column labels
df_matrix = df.pivot(index = "ITEM_CODE", columns = "ACCOUNTNUM", values = "TOTAL_QUANTITY")
df_matrix_norm = round((df_matrix - df_matrix.min())/(df_matrix.max() - df_matrix.min()), 4)

df_matrix_norm = round((df_matrix - 1)/(df_matrix.max() - 1), 4)


ddf = df_matrix_norm.T
ddf.reset_index(inplace = True)
data_norm = pd.melt(ddf, id_vars = ["ACCOUNTNUM"], value_name = "TOTAL_QUANTITY").dropna()

rdr = sp.Reader(rating_scale = (0, 1))
#ds = sp.Dataset.load_from_df(data_norm, rdr)
ds = sp.Dataset.load_from_df(data_norm, rdr)

param_grid = {
        "n_epochs": [5, 10],
        "lr_all": [0.002, 0.005],
        "reg_all": [0.4, 0.6]
    }

gs = sp.model_selection.GridSearchCV(sp.SVD, param_grid, measures = ["rmse", "mae"], cv = 3)
gs.fit(ds)

gs.best_params
gs.best_score

algo = sp.SVD()
sp.model_selection.cross_validate(algo, ds, measures = ["RMSE", "MAE"], cv=5, verbose=True)

train_set, test_set = sp.model_selection.train_test_split(ds, test_size = 0.3)
algo.fit(train_set)
predictions = algo.test(test_set)

sp.accuracy.rmse(predictions)
df_p = pd.DataFrame(predictions, columns=['uid', 'iid', 'rui', 'est', 'details'])

trainset = ds.build_full_trainset()
algo.fit(trainset)

algo.predict(12104957, "1313366", r_ui=0, verbose=True)


unique_items = data_norm.ITEM_CODE.unique()
unique_reps = data_norm.ACCOUNTNUM.unique()
unique_items["key"] = 0
unique_reps["key"] = 0

unique_reps.merge(unique_items, on = key, how = outer)

algo.predict



df_p.head()
df_p[df_p.uid == 12104957]
#df_p[df_p.est != 30]
