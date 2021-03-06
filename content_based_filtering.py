import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

DIR = './data/'
SET = 'content_base_set.csv'

books_data = pd.read_csv(os.path.join(DIR, SET), nrows=10000)

# Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')

# Replace NaN with an empty string (if existst)
books_data['description'] = books_data['description'].fillna('')

# Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(books_data['description'])

# Output the shape of tfidf_matrix
# print(tfidf_matrix.shape)

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Construct a reverse map of indices and book titles
indices = pd.Series(
    books_data.index, index=books_data['title']).drop_duplicates()


# Function that takes in book title as input and outputs most similar books


def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the book that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the books based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar book
    sim_scores = sim_scores[1:11]

    # Get the book indices
    book_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar books
    return books_data[
        ['book_id', 'title', 'author', 'description', 'ratings_count', 'average_rating', 'num_pages', 'format',
         'is_ebook', 'image_url']].iloc[book_indices]
