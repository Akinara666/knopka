from flask import Blueprint, jsonify, request
from models import Movie
from utils.recommendations import get_recommendations
from utils.helpers import login_required

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/recommendations', methods=['GET'])
@login_required
def recommendations(user_id):
    # Get recommendations and apply pagination
    recommended_ids = get_recommendations(user_id)
    # Query only the movies in the current page
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
