import pandas as pd
import re
import os
import sys
import gzip
import json
import os

DIR = './data/'
NAME = 'merged_books_set'


def load_data(file_name, head=None):
    count = 0
    data = []
    with gzip.open(file_name) as fin:
        for l in fin:
            d = json.loads(l)
            count += 1
            data.append(d)

            if (head is not None) and (count > head):
                break
    return data


def getGenresFromObject(obj):
    if obj:
        return list(obj.keys())[0]

    return 'unknown'


def getAuthorIdFromArray(arr):
    if arr:
        return arr[0].get("author_id")


books = load_data(os.path.join(DIR, 'goodreads_books.json.gz'), 90000)
genres = load_data(os.path.join(DIR, 'goodreads_book_genres_initial.json.gz'), 90000)
authors = load_data(os.path.join(DIR, 'goodreads_book_authors.json.gz'), 90000)

books_data = pd.DataFrame(books)
books_genres = pd.DataFrame(genres)
books_authors = pd.DataFrame(authors)
books_interactions = pd.read_csv(os.path.join(DIR, 'goodreads_interactions.csv'), nrows=9000000)

books_interactions['book_id'] = books_interactions['book_id'].astype(int)
books_data['book_id'] = books_data['book_id'].astype(int)
books_genres['book_id'] = books_genres['book_id'].astype(int)

authors_list = list(books_authors)

# removing unnecessary columns
authors_list.remove('average_rating')
authors_list.remove('text_reviews_count')
authors_list.remove('ratings_count')

# creating new books_authors, based on 'slimmer' authors_list
books_authors = books_authors[authors_list]

interactions_list = list(books_interactions)

# removing unnecessary columns
interactions_list.remove('is_reviewed')

# creating new books_interactions, based on 'slimmer' interactions_list
books_interactions = books_interactions[interactions_list]

# Selecting only necessary columns from books_data
books_data = books_data[
    ['book_id', 'title', 'ratings_count', 'average_rating', 'description', 'num_pages', 'authors', 'format', 'is_ebook',
     'image_url']]

# Adding genres information to existing table
books_data = pd.merge(books_data, books_genres, on='book_id')

# Adding genres information to existing table
books_data = pd.merge(books_data, books_interactions, on='book_id')

# Map object to single string with genres
books_data['genres'] = books_data['genres'].apply(getGenresFromObject)

# Map array of authors to single author_id
books_data['authors'] = books_data['authors'].apply(getAuthorIdFromArray)

# Change name of column 'authors' to 'author_id'
books_data.rename(columns={'authors': 'author_id'}, inplace=True)

# Adding authors information to existing table
books_data = pd.merge(books_data, books_authors, on='author_id')

# Rename 'name' column to 'author'
books_data.rename(columns={'name': 'author'}, inplace=True)

books_data.to_csv(os.path.join(DIR, NAME), index=False)

print(pd.read_csv(os.path.join(DIR, NAME)))
