import random
from models import Movie

def get_recommendations(user_id):
    all_movie_ids = [movie.id for movie in Movie.query.all()]
    return random.sample(all_movie_ids, min(len(all_movie_ids), 1))
