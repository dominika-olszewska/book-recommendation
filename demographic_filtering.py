import matplotlib.pyplot as plt
import pandas as pd
import os

DIR = './data/'

# 'content_base_set is also good in this scenario'
SET = 'content_base_set.csv'

books_data = pd.read_csv(os.path.join(DIR, SET), nrows=20000)

print(books_data.head())

# C is the mean vote across the whole report
C = books_data['average_rating'].mean()
print('mean is: ', C)

# m is the minimum votes required to be listed in the chart;
m = books_data['ratings_count'].quantile(0.9)
print('m is: ', m)

# Now, we can filter out the movies that qualify for the chart
q_movies = books_data.copy().loc[books_data['ratings_count'] >= m]
print(q_movies.shape)

def weighted_rating(x, m=m, C=C):
    v = x['ratings_count']
    R = x['average_rating']
    # Calculation based on the IMDB formula
    return (v / (v + m) * R) + (m / (m + v) * C)


# Define a new feature 'score' and calculate its value with `weighted_rating()`
q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

# Sort movies based on score calculated above
q_movies = q_movies.sort_values('score', ascending=False)

def getTopBooks():
  return q_movies[['book_id', 'title', 'author', 'description', 'ratings_count', 'average_rating', 'num_pages', 'format', 'is_ebook', 'image_url']].head(10)

#Drawing a chart
# pop = q_movies.sort_values('score', ascending=False)
# plt.figure(figsize=(12, 4))

# plt.barh(pop['title'].head(6), pop['score'].head(6), align='center',
#          color='skyblue')
# plt.gca().invert_yaxis()
# plt.xlabel("Popularity")
# plt.title("Popular Movies")

# plt.show()
