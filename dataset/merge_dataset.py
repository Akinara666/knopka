import pandas as pd

rating_df = pd.read_csv('title_ratings.tsv', sep='\t', low_memory=False)
titles_df = pd.read_csv('title_basics_cleaned.tsv', sep='\t', low_memory=False)

merged_df = pd.merge(titles_df, rating_df, on='tconst', how='inner')


print(merged_df.head())


merged_df.to_csv('title_ratings_basics.tsv', sep='\t', index=False)