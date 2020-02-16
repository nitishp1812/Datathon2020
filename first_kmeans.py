import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
 
# code for running kmeans on the complete dataset

data = pd.read_csv("score_data.csv")
zip_map = {}

for i in range(len(data)):
    zip_map[(data.iloc[i, 1], data.iloc[i, 2])] = data.iloc[i, 0]

data.head()
pop =  data['score'].values
nums = data['population'].values
X = np.array(list(zip(pop, nums)))
clstr = 3
c_x = np.random.randint(0, np.max(X) - 20, size=clstr)
c_y = np.random.randint(0, np.max(X) - 20, size=clstr)
C = np.array(list(zip(c_x, c_y)), dtype=np.float32)
plt.scatter(pop, nums, c = '#050505', s=20)
plt.scatter(c_x, c_y, marker='*', s=200, c="g")
 
kmeans = KMeans(n_clusters = clstr)
kmeans = kmeans.fit(X)
labels = kmeans.predict(X)
centroids = kmeans.cluster_centers_
 
colors = ['r', 'g', 'b', 'y', 'm', 'c', 'o', 'w']
figure = plt.figure()
kx = figure.add_subplot(111)
points = None
for i in range(clstr):
    points = np.array([X[j] for j in range(len(X)) if labels[j] == i])
    kx.scatter(points[:,0], points[:,1], s=20, cmap='rainbow')
kx.scatter(centroids[:,0], centroids[:,1], marker='*', s=200, c = '#050505')
plt.show()

zips = list()
for point in points:
    pop, score = point
    zips.append(zip_map[(pop, score)])

# generate CSV for best cluster
new_data = []
for i in range(len(data)):
    zip_val, popu, scor = data.iloc[i, 0], data.iloc[i, 2], data.iloc[i, 1]
    if zip_val in zips:
        new_data.append([zip_val, scor, popu])

new_df = pd.DataFrame(new_data, columns=['zipcode', 'score', 'population'])
new_df.to_csv('first_cluster.csv', index=False)
