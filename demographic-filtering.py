import matplotlib.pyplot as plt
import pandas as pd

# Demographic Filtering

books_data = pd.read_csv('books.csv')
books_data = books_data[
    ['book_id', 'title', 'ratings_1', 'ratings_2', 'ratings_3', 'ratings_4', 'ratings_5', 'average_rating']]

ratings_list = list(books_data)
ratings_list.remove('book_id')
ratings_list.remove('average_rating')

books_data['vote_count'] = books_data[ratings_list].sum(axis=1)

# C is the mean vote across the whole report
C = books_data['average_rating'].mean()
print('mean is: ', C)

# m is the minimum votes required to be listed in the chart;
m = books_data['vote_count'].quantile(0.9)
print('m is: ', m)

# Now, we can filter out the books that qualify for the chart
q_books = books_data.copy().loc[books_data['vote_count'] >= m]
print(q_books.shape)


def weighted_rating(x, m=m, C=C):
    v = x['vote_count']
    R = x['average_rating']
    # Calculation based on the IMDB formula
    return (v / (v + m) * R) + (m / (m + v) * C)


# Define a new feature 'score' and calculate its value with `weighted_rating()`
q_books['score'] = q_books.apply(weighted_rating, axis=1)

# Sort books based on score calculated above
q_books = q_books.sort_values('score', ascending=False)

# Print the top 15 books
print(q_books[['title', 'vote_count', 'average_rating', 'score']].head(10))

pop = q_books.sort_values('score', ascending=False)
plt.figure(figsize=(8, 4))

plt.barh(pop['title'].head(6), pop['score'].head(6), align='center',
         color='skyblue')
plt.gca().invert_yaxis()
plt.xlabel("Popularity")
plt.title("Popular Books")

plt.show()
