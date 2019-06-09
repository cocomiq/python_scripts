"""
This script perfoms the basic process for applying a machine learning
algorithm to a dataset using Python libraries.

The four steps are:
   1. Download a dataset (using pandas)
   2. Process the numeric data (using numpy)
   3. Train and evaluate learners (using scikit-learn)
   4. Plot and compare results (using matplotlib)


The data is downloaded from URL, which is defined below. As is normal
for machine learning problems, the nature of the source data affects
the entire solution. When you change URL to refer to your own data, you
will need to review the data processing steps to ensure they remain
correct.

============
Example Data
============
The example is from http://mlr.cs.umass.edu/ml/datasets/Water+Treatment+Plant
It contains a range of continuous values from sensors at a water
treatment plant, and the aim is to use unsupervised learners to
determine whether the plant is operating correctly. See the linked page
for more information about the data set.

This script uses unsupervised clustering learners and dimensionality
reduction models to find similar values, outliers, and visualize the
classes.
"""

# Remember to update the script for the new data when you change this URL
URL = "http://mlr.cs.umass.edu/ml/machine-learning-databases/water-treatment/water-treatment.data"

# Uncomment this call when using matplotlib to generate images
# rather than displaying interactive UI.
#import matplotlib
#matplotlib.use("Agg")

from pandas import read_table
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

try:
    # [OPTIONAL] Seaborn makes plots nicer
    import seaborn
except ImportError:
    pass


# =====================================================================
# 1. Download a dataset (using pandas)
# =====================================================================

def download_data(URL):
    """
    Downloads the data for this script into a pandas DataFrame.
    """

    # If your data is in an Excel file, install "xlrd" and use
    # pandas.read_excel instead of read_table
    #from pandas import read_excel
    #frame = read_excel(URL)

    # If your data is in a private Azure blob, install "azure" and use
    # BlobService.get_blob_to_path() with read_table() or read_excel()
    #import azure.storage
    #service = azure.storage.BlobService(ACCOUNT_NAME, ACCOUNT_KEY)
    #service.get_blob_to_path(container_name, blob_name, "my_data.csv")
    #frame = read_table("my_data.csv", ...

    # If your data is in a SQL DB, install "sqlalchemy" and use read_sql
    # pandas.read_sql instead of read_table
    #import sqlalchemy as sa     # required to use sqlalchemy queries
    #from pandas import read_sql
    #db = sa.create_engine("mysql+mysqldb://user:password@localhost/dbname")
    #results = sa.Table("results", metadata, autoload = True)
    # Accessing data via sqlalchemy queries
    #query_str = results.select(results.c.name == "test")
    # Using hard-coded SQL queries
    #query_str = "SELECT 1"
    #frame = read_sql(query_str, db)

    frame = read_table(
        URL,
        
        # Uncomment if the file needs to be decompressed
        #compression = "gzip",
        #compression = "bz2",

        # Specify the file encoding
        # Latin-1 is common for data from US sources
        #encoding = "latin-1",
        encoding = "utf-8",     # UTF-8 is also common

        # Specify the separator in the data
        sep = ",",              # comma separated values
        #sep = ";",             # semicolon separated values
        #sep = "\t",            # tab separated values
        #sep = " ",             # space separated values

        # Uncomment if the file has different decimal seperator rather than "."
        #decimal = ",",         # European seperator

        # Ignore spaces after the separator
        skipinitialspace = True,

        # Treat question marks as missing values
        na_values = ["?"],

        # Generate row labels from each row number
        index_col = None,
        #index_col = 0,         # use the first column as row labels
        #index_col = -1,        # use the last column as row labels

        # Generate column headers row from each column number
        header = None,
        
        # Skip commented and blank lines and use the first line of data as headers, by default it will skip blank lines
        #skip_blank_lines = True,
        #header = 0,
        
        # Use manual headers if column headers are not in data
        #header = None,
        #names = ["col1", "col2", ...],

        # Use manual headers and skip the first row in the file
        #header = 0,
        #names = ["col1", "col2", ...],
    )

    # Return a subset of the columns
    #return frame[["col1", "col4", ...]]

    # Return the entire frame
    #return frame

    # Return all except the first column
    del frame[frame.columns[0]]
    return frame


# =====================================================================
# 2. Process the numeric data (using numpy)
# =====================================================================

def get_features(frame):
    """
    Transforms and scales the input data and returns a numpy array that
    is suitable for use with scikit-learn.

    Note that in unsupervised learning there are no labels.
    """

    # Replace missing values with 0.0
    # or we can use scikit-learn to calculate missing values below
    #frame[frame.isnull()] = 0.0

    # Convert values to floats
    arr = np.array(frame, dtype=np.float)

    # Impute missing values from the mean of their entire column
    from sklearn.preprocessing import Imputer
    imputer = Imputer(strategy = "mean")  # "mean", "median", "most_frequent"
    arr = imputer.fit_transform(arr)
    
    # Normalize the entire data set to mean=0.0 and variance=1.0
    from sklearn.preprocessing import scale
    arr = scale(arr)

    return arr


def normalize_dimensions(X):
    """
    Normalizes dimensions of X with different normalization techniques.

    Returns a sequence of tuples containing:
        (title, x coordinates, y coordinates)
    for each normalizer. 
    """

    # Normalization is a rescaling of the data from the original range 
    # so that all values are within the range of 0 and 1.
    from sklearn.preprocessing import MinMaxScaler
    normalizer = MinMaxScaler(feature_range = (0, 2))
    #normalizer = normalizer.fit(X)
    #print("Min: %f, Max: %f" % (normalizer.data_min_, normalizer.data_max_))
    #normalized = normalizer.transform(X)
    normalized = normalizer.fit_transform(X)
    yield "min_max", normalized[:, 0], normalized[:, 1]

    # Standardizing a dataset involves rescaling the distribution of values 
    # so that the mean of observed values is 0 and the standard deviation is 1.
    from sklearn.preprocessing import StandardScaler
    normalizer = StandardScaler()
    #normalizer = normalizer.fit(X)
    #print("Mean: %f, StandartDeviation: %f" % (normalizer.mean_, normalizer.var_))
    #normalized = normalizer.transform(X)
    normalized = normalizer.fit_transform(X)
    yield "std_scaler", normalized[:, 0], normalized[:, 1]


# =====================================================================
# 3. Train and evaluate learners (using scikit-learn)
# =====================================================================

def reduce_dimensions(X):
    """
    Reduces the dimensionality of X with different reducers.

    Returns a sequence of tuples containing:
        (title, x coordinates, y coordinates)
    for each reducer.
    """

    # Principal Component Analysis (PCA) is a linear reduction model
    # that identifies the components of the data with the largest
    # variance.
    from sklearn.decomposition import PCA
    reducer = PCA(n_components = 2)
    X_r = reducer.fit_transform(X)
    yield "PCA", X_r[:, 0], X_r[:, 1]

    # Independent Component Analysis (ICA) decomposes a signal by
    # identifying the independent contributing sources.
    from sklearn.decomposition import FastICA
    reducer = FastICA(n_components = 2)
    X_r = reducer.fit_transform(X)
    yield "ICA", X_r[:, 0], X_r[:, 1]

    # FeatureUnion is a method to combine 2 different reduction method
    #from sklearn.pipeline import FeatureUnion
    #combined_features = FeatureUnion([("PCA", reducer_pca), ("ICA", redure_ica)])
    #X_r = combined_features.fit_transform(X)

    # Linear Discriminant Analysis is supervised linear dimensionality 
    # reduction model that tries to identify attributes that account for the most
    # variance between classes. It uses known class labels.
    # X should include class information, or another array can be used as class info.
    #from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    #reducer = LDA(n_components = 2)
    #X_r = reducer.fit_transform(X)
    #X_r = reducer.fit(X, y).transform(X)
    #yield "LDA", X_r[:, 0], X_r[:, 1]

    # Quadratic Dicrimination Analysis is other supervised linear dimensionality 
    # reduction model. It uses quadratic decision boundary, generated by fitting class 
    # conditional densities to the data and Bayes' rule.
    #from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
    #reducer = QDA()
    #X_r = reducer.fit(X, y).transform(X)

    # t-distributed Stochastic Neighbor Embedding (t-SNE) is a
    # non-linear reduction model. It operates best on data with a low
    # number of attributes (<50) and is often preceded by a linear
    # reduction model such as PCA.
    from sklearn.manifold import TSNE
    reducer = TSNE(n_components = 2)
    X_r = reducer.fit_transform(X)
    yield "t-SNE", X_r[:, 0], X_r[:, 1]


def evaluate_learners(X):
    """
    Run multiple times with different learners to get an idea of the
    relative performance of each configuration.

    Returns a sequence of tuples containing:
        (title, predicted classes)
    for each learner.
    """

    from sklearn.cluster import (MeanShift, MiniBatchKMeans, SpectralClustering, AgglomerativeClustering)

    learner = MeanShift(
        # Let the learner use its own heuristic for determining the
        # number of clusters to create
        bandwidth=None
    )
    y = learner.fit_predict(X)
    yield "Mean Shift clusters", y

    # Install HDBSCAN and import it
    # HDBSCAN, an updated version of DBSCAN
    #conda install -c conda-forge hdbscan
    #import hdbscan
    #yield "HDBSCAN clusters", y

    learner = MiniBatchKMeans(n_clusters = 2)
    y = learner.fit_predict(X)
    yield "K Means clusters", y

    learner = SpectralClustering(n_clusters = 2)
    y = learner.fit_predict(X)
    yield "Spectral clusters", y

    learner = AgglomerativeClustering(n_clusters = 2)
    y = learner.fit_predict(X)
    yield "Agglomerative clusters (N=2)", y

    learner = AgglomerativeClustering(n_clusters = 5)
    y = learner.fit_predict(X)
    yield "Agglomerative clusters (N=5)", y


# =====================================================================
# 4. Plot and compare results (using matplotlib)
# =====================================================================

def plot(Xs, predictions):
    """
    Create a plot comparing multiple learners.

    `Xs` is a list of tuples containing:
        (title, x coord, y coord)
    
    `predictions` is a list of tuples containing
        (title, predicted classes)

    All the elements will be plotted against each other in a
    two-dimensional grid.
    """

    # We will use subplots to display the results in a grid
    nrows = len(Xs)
    ncols = len(predictions)

    fig = plt.figure(figsize=(16, 8))
    fig.canvas.set_window_title("Clustering data from " + URL)

    # Show each element in the plots returned from plt.subplots()
    
    for row, (row_label, X_x, X_y) in enumerate(Xs):
        for col, (col_label, y_pred) in enumerate(predictions):
            ax = plt.subplot(nrows, ncols, row * ncols + col + 1)
            if row == 0:
                plt.title(col_label)
            if col == 0:
                plt.ylabel(row_label)

            # Plot the decomposed input data and use the predicted
            # cluster index as the value in a color map.
            plt.scatter(X_x, X_y, c=y_pred.astype(np.float), cmap="prism", alpha=0.5)
            
            # Set the axis tick formatter to reduce the number of ticks
            ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=4))

    # Let matplotlib handle the subplot layout
    plt.tight_layout()

    # ==================================
    # Display the plot in interactive UI
    plt.show()

    # To save the plot to an image file, use savefig()
    #plt.savefig("plot.png")

    # Open the image file with the default image viewer
    #import subprocess
    #subprocess.Popen("plot.png", shell=True)

    # To save the plot to an image in memory, use BytesIO and savefig()
    # This can then be written to any stream-like object, such as a
    # file or HTTP response.
    #from io import BytesIO
    #img_stream = BytesIO()
    #plt.savefig(img_stream, fmt="png")
    #img_bytes = img_stream.getvalue()
    #print("Image is {} bytes - {!r}".format(len(img_bytes), img_bytes[:8] + b"..."))

    # Closing the figure allows matplotlib to release the memory used.
    plt.close()


# =====================================================================

if __name__ == '__main__':
    # Download the data set from URL
    print("Downloading data from {}".format(URL))
    frame = download_data(URL)

    # Process data into a feature array
    # This is unsupervised learning, and so there are no labels
    print("Processing {} samples with {} attributes".format(len(frame.index), len(frame.columns)))
    X = get_features(frame)

    # Run multiple dimensionality reduction algorithms on the data
    print("Reducing dimensionality")
    Xs = list(reduce_dimensions(X))

    # Normalize dimensions of the data
    print("Normalizing dimensions")
    Xn = list(normalize_dimensions(Xs))

    # Standardize dimensions of the data
    print("Standardizing dimensions")

    # Evaluate multiple clustering learners on the data
    print("Evaluating clustering learners")
    predictions = list(evaluate_learners(X))

    # Display the results
    print("Plotting the results")
    plot(Xs, predictions)
