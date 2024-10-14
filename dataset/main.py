import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv('imdb_top_1000.csv')

df['Genre'] = df['Genre'].apply(lambda x: x.replace(' ', ''))
df['Actors'] = df['Star1'] + ' ' + df['Star2'] + ' ' + df['Star3'] + ' ' + \
               df['Star4']
df['features'] = df['Genre'] + ' ' + df['Director'] + ' ' + df['Star1'] + ' ' + df['Star2'] + ' ' + df['Star3'] + ' ' + \
                 df['Star4'] + ' ' + df['Overview']

# Создание отдельных TF-IDF матриц для каждого признака
tfidf_genre = TfidfVectorizer(stop_words='english')
tfidf_director = TfidfVectorizer(stop_words='english')
tfidf_actors = TfidfVectorizer(stop_words='english')

tfidf_matrix_genre = tfidf_genre.fit_transform(df['Genre'])
tfidf_matrix_director = tfidf_director.fit_transform(df['Director'])
tfidf_matrix_actors = tfidf_actors.fit_transform(df['Actors'])

# Применение весов к матрицам
weighted_genre = tfidf_matrix_genre * 2
weighted_director = tfidf_matrix_director * 1
weighted_actors = tfidf_matrix_actors * 1

# Объединение матриц (приведение их к одной форме через разреженные матрицы)
from scipy.sparse import hstack

combined_matrix = hstack([weighted_genre, weighted_director, weighted_actors])

cosine_sim = cosine_similarity(combined_matrix, combined_matrix)

# Создание словаря для быстрого поиска индекса по названию фильма
indices = pd.Series(df.index, index=df['Series_Title']).drop_duplicates()

# Функция для получения рекомендованных фильмов
def get_recommendations(title, cosine_sim=cosine_sim):
    # Получение индекса фильма
    idx = indices[title]
    # Получение схожести всех фильмов с данным
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Сортировка по уровню схожести
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Получение индексов фильмов (выбираем топ-10)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]

    # Возвращаем названия фильмов
    return df[['Series_Title', 'Genre', 'Director', 'Star1', 'Star2', 'Star3', 'Star4', 'Meta_score']].iloc[
        movie_indices]


# Пример использования функции
#print(df.loc[df['Series_Title'] == 'Drama, Action'])
print(get_recommendations('Fight Club'))

#TODO: чтобы был поиск либо по названию либо по жанрам а так же по актерам
