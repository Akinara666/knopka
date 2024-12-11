from flask import Blueprint, jsonify, request
from models import Movie
from utils.recommendations import get_recommendations
from utils.helpers import login_required

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/recommendations', methods=['GET'])
@login_required
def recommendations(user_id):
    # Get pagination parameters from the request
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # Get recommendations and apply pagination
    recommended_ids = get_recommendations(user_id)
    paginated_ids = recommended_ids[(page - 1) * per_page: page * per_page]

    # Query only the movies in the current page
    movies = Movie.query.filter(Movie.id.in_(paginated_ids)).all()
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
