import pandas as pd

# combine all files to create a CSV with all values
filenames = ["Part 1.csv", "Part 2.csv", "Part 3.csv", "Part 4a.csv", "Part 4b.csv", "Part 5.csv"]

dfs = []

for filename in filenames:
    df = pd.read_csv(filename)
    df = df.drop(0)
    dfs.append(df)

total_df = pd.concat(dfs)
total_df.to_csv('complete.csv', index=False)