import requests
import gzip
import shutil


resp = requests.get('https://datasets.imdbws.com/title.ratings.tsv.gz')

with open('data.gz', 'wb') as f:
  f.write(resp.content)



with gzip.open('data.gz', 'rb') as f_in:
    with open('title_ratings.tsv', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

