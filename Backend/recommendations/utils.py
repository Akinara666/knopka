def preprocess_user_data(user_data):
    """
    Preprocess user data for the recommendation model.
    :param user_data: Raw user data.
    :return: Processed features suitable for the model.
    """
    # Example preprocessing logic
    processed_data = {
        "age": user_data.get("age", 25),
        "liked_genres": user_data.get("liked_genres", []),
        "watched_movies": user_data.get("watched_movies", []),
    }
    # Convert to model-ready format
    return processed_data
