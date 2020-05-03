import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from surprise import SVD, Reader, Dataset

ratings_data = pd.read_csv('ratings-small.csv')
ratings_data.head()

books_all = pd.read_csv('books.csv')
books_all.head()

books_name = pd.read_csv('books.csv')
books_name = books_name[['book_id', 'title']]
books_name.head()

books_data = pd.merge(ratings_data, books_name, on='book_id')

reader = Reader()
data = Dataset.load_from_df(books_data[['user_id', 'book_id', 'rating']], reader)