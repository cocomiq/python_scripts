import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.plotly as py 
import plotly.graph_objs as go
from itertools import cycle

from sklearn import preprocessing
from sklearn import cluster
from sklearn import mixture

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from sklearn.cluster import (MeanShift, MiniBatchKMeans, SpectralClustering, AgglomerativeClustering)

# =====================================================================
# 1. Download a dataset (using pandas)
# =====================================================================

# url = "https://s3.amazonaws.com/happiness-report/2019/Chapter2OnlineData.xls"
# df = pd.read_excel(url)

df = pd.read_excel(r"C:\Users\acikgozs\Documents\Chapter2OnlineData.xls")


# =====================================================================
# 2. Visualize raw data
# =====================================================================

# ===== Correlation graph =====
cor = df.corr()
sns.heatmap(cor,square = True)
#cor.to_csv(r"C:\Users\acikgozs\Documents\test.csv")

# ===== Plotly World Map =====
data = [go.Choropleth(
    locations = df["Country name"], 
    locationmode = "country names", 
    z = df["Life Ladder"], 
    text = df["Country name"],
    colorbar = go.choropleth.ColorBar(title = "Happiness Index")
)]

layout = go.Layout(
    title = go.layout.Title(text = "Happiness Index 2018"), 
    geo = go.layout.Geo(showframe = False, projection = go.layout.geo.Projection(type = "equirectangular"))
)

choromap3 = go.Figure(data = data, layout = layout)
py.iplot(choromap3)


# =====================================================================
# 3. Process data
# =====================================================================

df_trans = df.groupby("Country name").transform(lambda x: x.fillna(x.mean()))
df_trans.dropna(inplace = True)


# =====================================================================
# 3.a. Dimension reduction
# =====================================================================

reducer_p = PCA(n_components = 2)
pca_df = reducer_p.fit_transform(df_trans)

# reducer_t = TSNE(n_components = 2)
# tsne_df = reducer_t.fit_transform(pca_df)


# =====================================================================
# 3.b. Manual Dimension selection
# =====================================================================

subdf = df_trans[["Life Ladder", "Log GDP per capita", "Social support", "Healthy life expectancy at birth", "Freedom to make life choices", "Generosity", "Perceptions of corruption", "Confidence in national government"]]
subdf.fillna(0, inplace = True)

scaler = preprocessing.StandardScaler()

scaled_df = scaler.fit_transform(subdf)

reducer_p = PCA(n_components = 2)
pca_df = reducer_p.fit_transform(scaled_df)


# =====================================================================
# 5. Clustering
# =====================================================================

learner = MeanShift(bandwidth = None)
ms = learner.fit_predict(pca_df)

learner = MiniBatchKMeans(n_clusters = 3)
mbkm = learner.fit_predict(pca_df)

learner = SpectralClustering(n_clusters = 3)
sc = learner.fit_predict(pca_df)

learner = AgglomerativeClustering(n_clusters = 3)
ac = learner.fit_predict(pca_df)


# =====================================================================
# 5. Cluster graphs
# =====================================================================

# Meanshift Results
fig = plt.figure(figsize=(16, 8))
fig.canvas.set_window_title("Clustering data from WHI")

plt.scatter(pca_df[:, 0], pca_df[:, 1], c = ms.astype(np.float))