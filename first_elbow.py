import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import cdist
import seaborn as sns
import matplotlib.pyplot as plt

# code for running the elbow method on the complete dataset

data = pd.read_csv("score_data.csv")

data.head()
pop =  data['score'].values
nums = data['population'].values
X = np.array(list(zip(pop, nums)))
clstr = range(1, 10)
distortions = []
c_x = np.random.randint(0, np.max(X) - 20, size=clstr)
c_y = np.random.randint(0, np.max(X) - 20, size=clstr)
C = np.array(list(zip(c_x, c_y)), dtype=np.float32)
plt.scatter(pop, nums, c = '#050505', s=20)
plt.scatter(c_x, c_y, marker='*', s=200, c="g")

for ctr in clstr:
    kmeansmodel = KMeans(n_clusters = ctr)
    kmeansmodel = kmeansmodel.fit(X)
    distortions.append(sum(np.min(cdist(X, kmeansmodel.cluster_centers_, 'euclidean'), axis = 1))/X.shape[0])

colors = ['r', 'g', 'b', 'y', 'm', 'c', 'o', 'w']
figure = plt.figure()
kx = figure.add_subplot(111)
kx.plot(clstr, distortions, 'b*-')
plt.grid(True)
plt.show()