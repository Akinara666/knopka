import pandas as pd
from flask import Blueprint, jsonify
from recommendations.model import MovieRecommender  # Path to your MovieRecommender class
from models import db, Movie, UserLikes
from utils.helpers import login_required

movies_bp = Blueprint('movies', __name__)

# Load the top_1000_imdb_movies.csv into a Pandas DataFrame
TOP_1000_IMDB_PATH = 'recommendations/data/top_1000_imdb_movies.csv'  # Path to your CSV file
try:
    top_1000_imdb_movies = pd.read_csv(TOP_1000_IMDB_PATH)
    print(f"Loaded {len(top_1000_imdb_movies)} movies from top_1000_imdb_movies.csv.")
except Exception as e:
    raise Exception(f"Failed to load top_1000_imdb_movies.csv: {e}")

# Initialize the MovieRecommender object
recommender = MovieRecommender(
    model_path='recommendations/data/knn_model.joblib',
    movies_path='recommendations/data/movies.csv',
    filtered_ratings_path='recommendations/data/filtered_ratings.csv',
    top_n=10
)


@movies_bp.route('/recommendations', methods=['GET'])
@login_required
def generate_recommendations(user_id):
    """
    Generate top-N movie recommendations for a user based on their favorite movies.
    Requires the user to be authenticated.

    Args:
        user_id (int): The authenticated user's ID, injected by the login_required decorator.

    Returns:
        JSON: A list of top-N recommended movies with their titles, tmdbId, and predicted ratings.
    """
    try:
        # Fetch the user's favorite movies from the database
        favorite_movies = UserLikes.query.filter_by(user_id=user_id).all()
        if not favorite_movies:
            return jsonify({"error": "User has no favorite movies."}), 404

        # Convert favorite movies to a dictionary {movieId: rating}
        user_ratings = {movie.movie_id: 5.0 for movie in favorite_movies}  # Default rating is 5.0

        # Generate recommendations using the recommender system
        recommendations = recommender.recommend(user_ratings)
        print(recommendations)
        # Extract tmdbId for each recommended movie from top_1000_imdb_movies.csv
        recommendations = recommendations.merge(
            top_1000_imdb_movies[['movieId', 'tmdbId']],
            left_on='movieId',
            right_on='movieId',
            how='left'
        )
        print(recommendations)
        # Drop rows where tmdbId is missing
        recommendations = recommendations.dropna(subset=['tmdbId'])

        # Convert tmdbId to integer
        recommendations['tmdbId'] = recommendations['tmdbId'].astype(int)

        print(recommendations)

        # Fetch movie details from the Movie database table
        tmdb_ids = recommendations['tmdbId'].tolist()
        movies = Movie.query.filter(Movie.tmdbId.in_(tmdb_ids)).all()
        # Create a list of movie details
        movie_list = []
        for movie in movies:
            movie_list.append({
                "id": movie.id,
                "tmdbId": movie.tmdbId,
                "title": movie.title,
                "description": movie.description,
                "image_url": movie.image_url,
                "rating": movie.rating,
                "trailer_url": movie.trailer_url,  # Include trailer URL
                "genres": movie.genres,  # Include genres
            })

        return jsonify(movie_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
