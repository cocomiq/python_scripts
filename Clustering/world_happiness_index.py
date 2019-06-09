import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.plotly as py 
import plotly.graph_objs as go

from sklearn import preprocessing
from sklearn import cluster
from sklearn import mixture

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from sklearn.cluster import (MeanShift, MiniBatchKMeans, SpectralClustering, AgglomerativeClustering)

# =====================================================================
# 1. Download a dataset (using pandas)
# =====================================================================

df = pd.read_excel(r"C:\Users\acikgozs\Documents\Chapter2OnlineData.xls")


# =====================================================================
# 2. Visualize raw data
# =====================================================================

cor = df.corr()
sns.heatmap(cor,square = True)
#cor.to_csv(r"C:\Users\acikgozs\Documents\test.csv")

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

reducer_t = TSNE(n_components = 2)
tsne_df = reducer_t.fit_transform(pca_df)


# =====================================================================
# 3.b. Manual Dimension reduction
# =====================================================================

subdf = df_trans[["Life Ladder", "Log GDP per capita", "Social support", "Healthy life expectancy at birth", "Freedom to make life choices", "Generosity", "Perceptions of corruption", "Confidence in national government"]]
subdf.fillna(0, inplace = True)

scaler = preprocessing.StandardScaler()

scaled_df = scaler.fit_transform(subdf)


# =====================================================================
# 5. Clustering
# =====================================================================

learner = MeanShift(
        # Let the learner use its own heuristic for determining the
        # number of clusters to create
        bandwidth=None
    )

ms = learner.fit_predict(pca_df)