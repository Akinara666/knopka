import os
import requests
from models import db, Movie
from app import create_app

# Set your TMDB API key
TMDB_API_KEY = "ea5079d0926cb2d553f605868693a9f6"  # Replace with your actual API key
TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_FOLDER = "static/movie_images"  # Define a folder for saving images

# Ensure the image folder exists
os.makedirs(IMAGE_FOLDER, exist_ok=True)

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
        "sort_by": "vote_count.desc",
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
        "language": "en-US",
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json().get("results", [])
        for video in results:
            if video.get("site") == "YouTube" and video.get("type") == "Trailer":
                return f"https://www.youtube.com/watch?v={video.get('key')}"
    return None

def fetch_genres():
    """
    Fetch genres and their IDs from TMDB API.
    Returns a dictionary mapping genre IDs to genre names.
    """
    url = f"{TMDB_BASE_URL}/genre/movie/list"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "ru-RU"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        return {genre["id"]: genre["name"] for genre in genres}
    else:
        print(f"Error fetching genres: {response.status_code}")
        return {}

def map_genres_to_ids(movie_genres, genre_mapping):
    """
    Map TMDB genre IDs in a movie to their corresponding genre names.
    :param movie_genres: List of genre IDs for a movie.
    :param genre_mapping: Dictionary of {genre_id: genre_name}.
    :return: Comma-separated string of genre names.
    """
    return ", ".join([genre_mapping.get(genre_id, "Unknown") for genre_id in movie_genres])


def download_image(image_url, tmdb_id):
    """
    Download an image and save it to the IMAGE_FOLDER with a unique name.
    :param image_url: The URL of the image to download.
    :param tmdb_id: The unique TMDB ID of the movie for naming the file.
    :return: The file path of the downloaded image or None if the download fails.
    """
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(IMAGE_FOLDER, f"{tmdb_id}.jpg")
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return file_path
        else:
            print(f"Failed to download image: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def add_movie_to_db(movie, genre_mapping):
    """
    Add a single movie to the database with mapped genres and trailer.
    :param movie: A dictionary containing movie details from TMDB.
    :param genre_mapping: Dictionary of {genre_id: genre_name}.
    """
    tmdb_id = movie.get("id")
    title = movie.get("title")
    description = movie.get("overview")
    genres = map_genres_to_ids(movie.get("genre_ids", []), genre_mapping)
    image_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None
    local_image_path = download_image(image_url, tmdb_id) if image_url else None
    trailer_url = fetch_trailer(movie.get("id"))  # Fetch the trailer
    rating = movie.get("vote_average", 0.0)

    # Check for existing movie by TMDB ID
    existing_movie = Movie.query.filter_by(tmdbId=tmdb_id).first()
    if existing_movie:
        print(f"Movie '{title}' (TMDB ID: {tmdb_id}) already exists in the database.")
        return

    new_movie = Movie(
        tmdbId=tmdb_id,  # Save the TMDB ID
        title=title,
        description=description,
        genres=genres,
        image_url=local_image_path,
        trailer_url=trailer_url,  # Include the trailer URL
        rating=rating
    )
    db.session.add(new_movie)
    db.session.commit()
    print(f"Added movie: {title} (TMDB ID: {tmdb_id})")


def populate_movies_database(total_pages=1):
    """
    Populate the movies database with data from TMDB.
    :param total_pages: Number of pages to fetch from TMDB (default: 1).
    """
    with app.app_context():
        # Fetch genre mapping
        genre_mapping = fetch_genres()
        if not genre_mapping:
            print("Failed to fetch genres. Exiting.")
            return

        for page in range(1, total_pages + 1):
            print(f"Fetching page {page}...")
            movies = fetch_movies(page=page)
            for movie in movies:
                add_movie_to_db(movie, genre_mapping)
        print("Movies database population complete.")


if __name__ == "__main__":
    populate_movies_database(total_pages=50)  # Adjust the number of pages based on your requirements