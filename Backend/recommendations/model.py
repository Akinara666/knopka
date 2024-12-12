import joblib
from surprise import SVD, Dataset, Reader

MODEL_PATH = "best_svd_model_with_mappings.pkl"  # Path to your saved model file

class RecommendationModel:
    def __init__(self):
        """
        Initialize the RecommendationModel by loading the serialized model and mappings.
        """
        self.model = None
        self.user_id_to_index = {}
        self.movie_id_to_index = {}
        self.index_to_user_id = {}
        self.index_to_movie_id = {}
        self._load_model()

    def _load_model(self):
        """
        Load the serialized model and mappings using joblib.
        """
        try:
            model_data = joblib.load(MODEL_PATH)
            self.model = model_data["model"]
            self.user_id_to_index = model_data["user_id_to_index"]
            self.movie_id_to_index = model_data["movie_id_to_index"]
            self.index_to_user_id = model_data["index_to_user_id"]
            self.index_to_movie_id = model_data["index_to_movie_id"]
            print("Model and mappings loaded successfully.")
        except Exception as e:
            print(f"Error loading model and mappings: {e}")

    def get_recommendations(self, liked_movies, top_n=10):
        """
        Generate movie recommendations based on user-liked movies.
        Recommendations are made using the SVD model's predictions.

        :param liked_movies: List of movie IDs the user likes.
        :param top_n: Number of recommendations to generate.
        :return: List of recommended movie IDs.
        """
        if not self.model:
            raise ValueError("Model is not loaded.")

        # Check if liked_movies contains valid movie IDs
        if not liked_movies:
            raise ValueError("No liked movies provided for recommendations.")

        # Ensure liked movies exist in the model's movie mappings
        valid_liked_movies = [
            movie_id for movie_id in liked_movies if movie_id in self.movie_id_to_index
        ]
        if not valid_liked_movies:
            raise ValueError("None of the liked movies are recognized by the model.")

        # Predict ratings for all unseen movies
        candidate_movie_ids = set(self.movie_id_to_index.keys()) - set(valid_liked_movies)
        predictions = []

        for candidate_movie_id in candidate_movie_ids:
            # Predict rating based on the average score of liked movies
            candidate_inner_id = self.movie_id_to_index[candidate_movie_id]
            score = 0
            for liked_movie_id in valid_liked_movies:
                liked_inner_id = self.movie_id_to_index[liked_movie_id]
                prediction = self.model.predict(0, candidate_inner_id)  # Predict for a dummy user
                score += prediction.est  # `est` is the predicted rating

            # Average the scores
            score /= len(valid_liked_movies)
            predictions.append((candidate_movie_id, score))

        # Sort by predicted rating in descending order and return the top N movie IDs
        predictions.sort(key=lambda x: x[1], reverse=True)
        return [movie_id for movie_id, _ in predictions[:top_n]]



if __name__ == '__main__':
    model = RecommendationModel()
    rec = model.get_recommendations([92259, 68954, 99114])
    print(rec)