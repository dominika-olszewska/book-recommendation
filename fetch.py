import pandas as pd
import os

DIR = './data/'
SET = 'content_base_set.csv'

books_data = pd.read_csv(os.path.join(DIR, SET), nrows=10000)


def get_random_book():
    return books_data[
        ['book_id', 'title', 'author', 'description', 'ratings_count', 'average_rating', 'num_pages', 'format',
         'is_ebook', 'image_url']].sample()


def getBookByID(id):
    return books_data.loc[books_data['book_id'] == id]


def getBookByTitle(title):
    return books_data.loc[books_data['title'] == title]


def getBooksByAuthor(author):
    return books_data.loc[books_data['author'] == author]


def getBooks():
    return books_data
