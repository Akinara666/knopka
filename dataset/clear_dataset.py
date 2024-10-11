import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv('title_ratings_basics.tsv', sep='\t', low_memory=False)
print(df.head())
print(df.describe())
print(df.info())

exclude_type = ['tvEpisode', 'tvSpecial', 'music', 'video']
exclude_genre = []
df = df.loc[(df['averageRating'] >= 5.0) & (df['startYear'] >= '1980') & (~df['titleType'].isin(exclude_type))]
df = df.loc[df['genres'].apply(lambda x: not any(t in x.split(',') for t in exclude_genre))]

print(df.head(100))
print(df.describe())
print(df.info())
print(df.isnull().sum())

df_sorted = df.sort_values('averageRating', ascending=False)
print(df_sorted.head(100))
print(df_sorted.describe())

df_sorted.to_csv('title_cleared_sorted.tsv', sep='\t', index=False)

