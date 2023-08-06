from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import re
import joblib
import os
import sys


def load_csv():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'processed_anime.csv')
    anime_data = pd.read_csv(data_path)
    return anime_data

# Define the give_rec function to recommend anime based on similarity to input title


def give_rec(title):
    # Get the index corresponding to anime title
    idx = indices[title]

    # Get the pairwsie similarity scores
    sig_scores = list(enumerate(sig[idx]))

    # Sort the anime based on similarity scores
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of top 10 most similar anime excluding the input anime
    anime_indices = [i[0] for i in sig_scores[1:11]]

    # Create dataframe of top 10 recommended anime
    top_anime = pd.DataFrame({
        'Anime name': anime_data['Name'].iloc[anime_indices].values,
        'Rating': anime_data['Score'].iloc[anime_indices].values
    })

    return top_anime


def main():
    global indices
    global sig
    global anime_data
    anime_data = load_csv()
    tfv_file = 'tfv.joblib'
    sig_file = 'sig.joblib'
    indices_file = 'indices.joblib'

    print("Sys arg v len is", len(sys.argv))
    if len(sys.argv) < 2:
        print("Error: No search term provided")
        return

    if len(sys.argv) > 2:
        print("Please provide search term in quotation marks, example: 'One Punch Man' ")
        return

    if os.path.exists(tfv_file) and os.path.exists(sig_file) and os.path.exists(indices_file):
        print("*** Found existing joblib files, loading them... ***")
        tfv_matrix = joblib.load(tfv_file)
        sig = joblib.load(sig_file)
        indices = joblib.load(indices_file)
        print("*** Files loaded successfully! ***")

    else:
        print("*** Files not found, generating them..")
        genres_str = anime_data['Genres'].str.split(',').astype(str)

        # Initialize the TfidfVectorizer with various parameters
        tfv = TfidfVectorizer(min_df=3, max_features=None,
                              strip_accents='unicode', analyzer='word',
                              token_pattern=r'\w{1,}',
                              ngram_range=(1, 3),
                              stop_words='english')

        # Use the TfidfVectorizer to transform the genres_str into a sparse matrix
        tfv_matrix = tfv.fit_transform(genres_str)

        # Compute the sigmoid kernel
        sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

        # Create a Pandas Series object where the index is the anime names and the values are the indices in anime_data
        indices = pd.Series(anime_data.index, index=anime_data['Name'])
        indices = indices.drop_duplicates()

        joblib.dump(tfv_matrix, tfv_file)
        joblib.dump(sig, sig_file)
        joblib.dump(indices, indices_file)
        print("*** Files generated successfully! ***")

    search_term = sys.argv[1]
    try:
        recommendations = give_rec(search_term)
        print(f"\n\nRecommended anime similar to {search_term}:\n")
        print(recommendations)

    except KeyError:
        print(f"Sorry, {search_term} is not in our database.")


if __name__ == "__main__":
    main()
