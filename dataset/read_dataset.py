import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# chunksize = 100
# with pd.read_csv('title_basics.tsv', sep='\t', chunksize=chunksize) as reader:
#     for chunk in reader:
#       df = pd.DataFrame(chunk)
#       break


df = pd.read_csv('title_basics.tsv', sep='\t', low_memory=False)
print(df.head())
print(df.info())
print(df.describe())

df = df.loc[df['isAdult'] != '1']

df.to_csv('title_basics_cleaned.tsv', sep='\t', index=False)

print(df.head())
print(df.info())
print(df.describe())



