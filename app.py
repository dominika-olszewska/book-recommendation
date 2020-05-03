import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ratings_data = pd.read_csv('ratings-small.csv')
ratings_data.head()

books_name = pd.read_csv('books.csv')
books_name = books_name[['book_id', 'title']]
books_name.head()

books_data = pd.merge(ratings_data, books_name, on='book_id')
books_data.groupby('title')['rating'].count().sort_values(ascending=False).head()
