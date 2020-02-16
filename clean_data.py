import numpy as np
import pandas as pd

# clean the complete data (all data from all files)
df = pd.read_csv('complete.csv')

# clean RCPSZFE aggregates and useless data from total CSV
idx = df[df["RCPSZFE.id"] == 1].index
df.drop(idx, inplace=True)
idx = df[df["RCPSZFE.id"] == 2].index
df.drop(idx, inplace=True)
idx = df[df["RCPSZFE.id"] == 998].index
df.drop(idx, inplace=True)

# remove NAICS aggregates from CSV
indices = df[df['NAICS.id'] != "44-45"].index
df.drop(indices, inplace=True)

# remove unused columns
df.drop(columns=['NAICS.display-label', 'RCPSZFE.display-label', 'GEO.id', 'GEO.display-label', 'YEAR.id', 'NAICS.id'], inplace=True)

# mapping for RCPSZFE to weights
id_map = {
    114: 1,
    123: 1.75,
    125: 3.75,
    131: 7.5,
    132: 10
}

# compute the score for each establishent category per zipcode
df['RCPSZFE.id'] = df['RCPSZFE.id'].map(id_map)
df['SCORE'] = df['RCPSZFE.id'] * df['ESTAB']

# compute average score for each zipcode
zips, counts, pops = {}, {}, {}
for i in range(len(df)):
    if df.iloc[i, 1] in zips:
        zips[df.iloc[i, 1]] += df.iloc[i, -1]
        counts[df.iloc[i, 1]] += df.iloc[i, -2]
    else:
        zips[df.iloc[i, 1]] = df.iloc[i, -1]
        counts[df.iloc[i, 1]] = df.iloc[i, -2]

data = []

# create zipcode to population mapping
pop_df = pd.read_csv('pop_data.csv')
for i in range(len(pop_df)):
    pops[pop_df.iloc[i, 1]] = pop_df.iloc[i, 0]

# add average score, zipcode and population to new dataframe
for key in zips:
    if key in pops:
        data.append([key, zips[key] / counts[key], pops[key]])
    else:
        data.append([key, zips[key] / counts[key], np.nan])
new_df = pd.DataFrame(data, columns=['zipcode', 'score', 'population'])

# drop unusable data
idx = new_df[new_df['population'].isnull()].index
new_df.drop(idx, inplace=True)

# generate CSV for clean data
new_df.to_csv('score_data.csv', index=False)
