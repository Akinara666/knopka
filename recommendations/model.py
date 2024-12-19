import random

import pandas as pd
import joblib

# Paths to required files
model_file = 'data/knn_model.joblib'  # Path to your saved KNN model
movies_file = 'data/movies.csv'  # Path to movies.csv
filtered_ratings_file = 'data/filtered_ratings.csv'  # Path to your filtered ratings CSV


class MovieRecommender:
    """
    A movie recommendation system using a pre-trained KNN-based collaborative filtering model.

    Attributes:
        model_path (str): Path to the saved KNN model file.
        movies_path (str): Path to the MovieLens movies.csv file.
        filtered_ratings_path (str): Path to the filtered ratings CSV file.
        top_n (int): Number of recommendations to return.
    """

    def __init__(self, model_path, movies_path, filtered_ratings_path, top_n=10):
        """
        Initializes the MovieRecommender by loading the model and necessary data.

        Args:
            model_path (str): Path to the saved KNN model file.
            movies_path (str): Path to the MovieLens movies.csv file.
            filtered_ratings_path (str): Path to the filtered ratings CSV file.
            top_n (int, optional): Number of recommendations to return. Defaults to 10.
        """
        self.model_path = model_path
        self.movies_path = movies_path
        self.filtered_ratings_path = filtered_ratings_path
        self.top_n = top_n

        # Load the pre-trained KNN model
        try:
            self.algo = joblib.load(self.model_path)
            print(f"Model loaded successfully from {self.model_path}.")
        except FileNotFoundError:
            raise Exception(f"Model file not found at {self.model_path}.")
        except Exception as e:
            raise Exception(f"An error occurred while loading the model: {e}")

        # Load the movies DataFrame to map movieId to titles
        try:
            self.movies = pd.read_csv(self.movies_path)
            if not {'movieId', 'title'}.issubset(self.movies.columns):
                raise ValueError("movies.csv must contain 'movieId' and 'title' columns.")
            print(f"Movies data loaded successfully from {self.movies_path}.")
        except FileNotFoundError:
            raise Exception(f"Movies file not found at {self.movies_path}.")
        except Exception as e:
            raise Exception(f"An error occurred while loading movies data: {e}")

        # Load the filtered ratings to compute global mean
        try:
            self.filtered_ratings = pd.read_csv(self.filtered_ratings_path)
            if 'rating' not in self.filtered_ratings.columns:
                raise ValueError("Filtered ratings must contain a 'rating' column.")
            self.global_mean = self.filtered_ratings['rating'].mean()
            print(f"Filtered ratings loaded successfully from {self.filtered_ratings_path}.")
            print(f"Global mean rating computed: {self.global_mean:.2f}")
        except FileNotFoundError:
            raise Exception(f"Filtered ratings file not found at {self.filtered_ratings_path}.")
        except Exception as e:
            raise Exception(f"An error occurred while loading filtered ratings: {e}")

    def recommend(self, new_user_ratings):
        """
        Generates top-N movie recommendations for a new user based on their ratings.

        Args:
            new_user_ratings (dict): A dictionary where keys are movieIds and values are ratings.
                                     Example: {50: 5.0, 181: 4.0, 258: 3.0}

        Returns:
            pd.DataFrame: A DataFrame containing the top-N recommended movies with their titles and predicted ratings.
        """
        # Validate input
        if not isinstance(new_user_ratings, dict):
            raise ValueError("new_user_ratings must be a dictionary of {movieId: rating}.")

        # Extract all movieIds from the training set
        all_items = set(self.filtered_ratings['movieId'].unique())
        rated_items = set(new_user_ratings.keys())
        candidate_items = all_items - rated_items

        # Initialize a list to store predictions
        predictions_for_new_user = []

        # Iterate over each candidate movie to predict the rating
        for item_id in candidate_items:
            # Check if the item_id exists in the training set
            if item_id not in self.algo.trainset._raw2inner_id_items:
                continue  # Skip if the movie was not in the training set

            try:
                # Convert raw movieId to inner id used by Surprise
                inner_iid = self.algo.trainset.to_inner_iid(item_id)
            except ValueError:
                # If the movieId is unknown, skip
                continue

            # Get the top-k similar items (neighbors)
            k = random.randint(1000, 5000)  # You can adjust k based on your preference
            neighbors = self.algo.get_neighbors(inner_iid, k=k)

            numer = 0.0
            denom = 0.0
            for nb_iid in neighbors:
                nb_raw_iid = self.algo.trainset.to_raw_iid(nb_iid)
                if nb_raw_iid in new_user_ratings:
                    sim_score = self.algo.sim[inner_iid][nb_iid]
                    numer += sim_score * new_user_ratings[nb_raw_iid]
                    denom += abs(sim_score)

            if denom > 0:
                est_rating = numer / denom
            else:
                # Fallback to global mean rating if no similar items are rated
                est_rating = self.global_mean

            predictions_for_new_user.append((item_id, est_rating))

        # Convert predictions to DataFrame
        predictions_df = pd.DataFrame(predictions_for_new_user, columns=['movieId', 'predicted_rating'])

        # Sort the predictions by estimated rating in descending order
        predictions_df.sort_values(by='predicted_rating', ascending=False, inplace=True)

        # Select the top-N recommendations
        top_n_recommendations = predictions_df.head(self.top_n)

        # Merge with movies DataFrame to get movie titles
        top_n_recommendations = top_n_recommendations.merge(
            self.movies[['movieId', 'title']],
            on='movieId',
            how='left'
        )

        top_n_recommendations['title'] = top_n_recommendations['title'].fillna('Unknown Title')

        # Reorder columns for clarity
        top_n_recommendations = top_n_recommendations[['movieId', 'title', 'predicted_rating']]

        return top_n_recommendations.reset_index(drop=True)


if __name__ == '__main__':
    # Initialize the recommender system
    recommender = MovieRecommender(
        model_path=model_file,
        movies_path=movies_file,
        filtered_ratings_path=filtered_ratings_file,
        top_n=10  # Number of recommendations to generate
    )

    # Define new user ratings (movieId: rating)
    new_user_ratings = {
        1: 1.0,
        2: 5.0,
        3: 3.0
    }

    # Generate recommendations
    recommendations = recommender.recommend(new_user_ratings)

    # Display the recommendations
    print("Top 10 recommended movies for the new user:")
    print(recommendations)

