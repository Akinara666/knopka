from flask import Blueprint, jsonify, request
from recommendations.model import RecommendationModel
from recommendations.utils import preprocess_user_data
from models import Movie
from utils.helpers import login_required

movies_bp = Blueprint('movies', __name__)
model = RecommendationModel()

@movies_bp.route('/recommendations', methods=['GET'])
@login_required
def recommendations(user_id):
    # Fetch user data from the database
    user_data = {
        "liked_movies": [1, 50, 100],  # Example liked movie IDs from the database
    }

    try:
        # Generate recommendations
        liked_movies = user_data["liked_movies"]
        recommended_ids = model.get_recommendations(liked_movies, user_id)

        # Fetch movie details from the database
        movies = Movie.query.filter(Movie.id.in_(recommended_ids)).all()
        movie_list = [{
            'id': m.id,
            'title': m.title,
            'description': m.description,
            'genres': m.genres,
            'image_url': m.image_url,
            'trailer_url': m.trailer_url,
            'rating': m.rating
        } for m in movies]

        return jsonify(movie_list), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
