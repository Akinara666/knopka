import os
import requests
from models import db, Movie
from app import create_app

# Set your TMDB API key
TMDB_API_KEY = "ea5079d0926cb2d553f605868693a9f6"  # Replace with your actual API key
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Create the Flask app context
app = create_app()

def fetch_movies(page=1):
    """
    Fetch movies from TMDB API.
    :param page: The page number for pagination (default: 1)
    :return: List of movie dictionaries from TMDB
    """
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "ru-RU",
        "sort_by": "popularity.desc",
        "page": page,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error fetching data from TMDB: {response.status_code}")
        return []

def fetch_trailer(movie_id):
    """
    Fetch the trailer URL for a given movie ID from TMDB.
    :param movie_id: The TMDB ID of the movie
    :return: YouTube trailer URL or None if unavailable
    """
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/videos"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "ru-RU",
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json().get("results", [])
        if not results:
            params = {
                "api_key": TMDB_API_KEY,
                "language": "en-US",
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                results = response.json().get("results", [])
        for video in results:
            if video.get("site") == "YouTube" and video.get("type") == "Trailer":
                return f"https://www.youtube.com/watch?v={video.get('key')}"
    return None

def add_movie_to_db(movie):
    """
    Add a single movie to the database.
    :param movie: A dictionary containing movie details from TMDB
    """
    # Extract relevant details from TMDB response
    title = movie.get("title")
    description = movie.get("overview")
    genres = ", ".join([str(genre) for genre in movie.get("genre_ids", [])])  # Replace with actual genre mapping if needed
    image_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None
    trailer_url = fetch_trailer(movie.get("id"))
    rating = movie.get("vote_average", 0.0)

    # Check if movie already exists
    existing_movie = Movie.query.filter_by(title=title).first()
    if existing_movie:
        print(f"Movie '{title}' already exists in the database.")
        return

    # Add new movie to the database
    new_movie = Movie(
        title=title,
        description=description,
        genres=genres,
        image_url=image_url,
        trailer_url=trailer_url,
        rating=rating,
    )
    db.session.add(new_movie)
    db.session.commit()
    print(f"Added movie: {title}")

def populate_movies_database(total_pages=1):
    """
    Populate the movies database with data from TMDB.
    :param total_pages: Number of pages to fetch from TMDB (default: 1)
    """
    with app.app_context():
        for page in range(1, total_pages + 1):
            print(f"Fetching page {page}...")
            movies = fetch_movies(page=page)
            for movie in movies:
                add_movie_to_db(movie)
        print("Movies database population complete.")

if __name__ == "__main__":
    populate_movies_database(total_pages=10)  # Adjust the number of pages based on your requirements