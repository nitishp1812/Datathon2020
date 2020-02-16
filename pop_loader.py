import pandas as pd

# read the 2010 population data and generate a more usable CSV from that based on the data
df = pd.read_csv('population_by_zip_2010.csv')
df = df[df.gender.isnull()]
df.drop(columns=['minimum_age', 'maximum_age', 'gender'], inplace=True)

df.to_csv('pop_data.csv', index=False)