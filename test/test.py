import pytest
from app import create_app
from config import TestConfig
from models import db, User, Movie, UserLikes
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    """
    Create a test client and set up the database for testing.
    """
    app = create_app(config_class=TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            populate_test_data()
        yield client
        with app.app_context():
            db.drop_all()

def populate_test_data():
    """
    Populate the database with initial test data.
    """
    user = User(username="testuser", login="testlogin", password_hash=generate_password_hash("password123"))
    movie1 = Movie(id=1, tmdbId=101, title="Inception", genres="Action, Sci-Fi", rating=8.8, image_url="example.com/img1.jpg")
    movie2 = Movie(id=2, tmdbId=102, title="The Matrix", genres="Action, Sci-Fi", rating=8.7, image_url="example.com/img2.jpg")
    db.session.add_all([user, movie1, movie2])
    db.session.commit()

def login(client):
    """
    Helper function to log in and retrieve a token.
    """
    response = client.post('api/auth/login', json={"login": "testlogin", "password": "password123"})
    return response.json['token'] if response.status_code == 200 else None

def test_register_user(client):
    """
    Test user registration.
    """
    response = client.post('api/auth/register', json={
        "username": "newuser",
        "login": "newlogin",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'

def test_login_user(client):
    """
    Test user login.
    """
    response = client.post('/api/auth/login', json={"login": "testlogin", "password": "password123"})
    assert response.status_code == 200
    assert 'token' in response.json

def test_login_invalid_user(client):
    """
    Test login with invalid credentials.
    """
    response = client.post('/api/auth/login', json={"login": "testlogin", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json['error'] == 'Invalid credentials'

def test_get_random_movies(client):
    """
    Test fetching 20 random movies.
    """
    response = client.get('/api/movies/random-movies')
    assert response.status_code == 200
    assert len(response.json) == 2  # We populated 2 movies in test data

def test_search_movies(client):
    """
    Test searching for movies by title.
    """
    response = client.get('/api/movies/search?query=Inception')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['title'] == "Inception"

    response_empty = client.get('/api/movies/search?query=Nonexistent')
    assert response_empty.status_code == 200
    assert len(response_empty.json) == 0

def test_add_to_favorites(client):
    """
    Test adding a movie to the user's favorites.
    """
    token = login(client)
    assert token is not None

    headers = {"Authorization": f"{token}"}
    response = client.post('/api/movies/like', json={"movieId": 1}, headers=headers)
    assert response.status_code == 201
    assert response.json['message'] == "Movie 'Inception' added to your favorites."

    # Attempt to add the same movie again
    response_duplicate = client.post('/api/movies/like', json={"movieId": 1}, headers=headers)
    assert response_duplicate.status_code == 409
    assert response_duplicate.json['error'] == "This movie is already in your favorites."

def test_generate_recommendations(client):
    """
    Test fetching movie recommendations for a user.
    """
    token = login(client)
    assert token is not None

    headers = {"Authorization": f"{token}"}
    # Add a favorite movie
    client.post('/api/movies/like', json={"movieId": 1}, headers=headers)

    response_with_favorites = client.get('/api/movies/recommendations', headers=headers)
    assert response_with_favorites.status_code == 200
    assert isinstance(response_with_favorites.json, list)

def test_user_profile(client):
    """
    Test fetching the user profile.
    """
    token = login(client)
    assert token is not None

    headers = {"Authorization": f"{token}"}
    response = client.get('/api/user/profile', headers=headers)
    assert response.status_code == 200
    assert response.json['username'] == "testuser"
