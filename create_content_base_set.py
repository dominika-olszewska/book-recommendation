import pandas as pd
import gzip
import json
import os

DIR = './data/'
NAME = 'content_base_set.csv'


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


books = load_data(os.path.join(DIR, 'goodreads_books.json.gz'), 20000)
genres = load_data(os.path.join(DIR, 'goodreads_book_genres_initial.json.gz'), 200000)
authors = load_data(os.path.join(DIR, 'goodreads_book_authors.json.gz'), 200000)

books_data = pd.DataFrame(books)
books_genres = pd.DataFrame(genres)
books_authors = pd.DataFrame(authors)

authors_list = list(books_authors)

# removing unnecessary columns
authors_list.remove('average_rating')
authors_list.remove('text_reviews_count')
authors_list.remove('ratings_count')

# creating new books_authors, based on 'slimmer' authors_list
books_authors = books_authors[authors_list]

# Selecting only necessary columns from books_data
books_data = books_data[
    ['book_id', 'title', 'ratings_count', 'average_rating', 'description', 'num_pages', 'authors', 'format', 'is_ebook',
     'image_url']]

# Adding genres information to existing table
books_data = pd.merge(books_data, books_genres, on='book_id')

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