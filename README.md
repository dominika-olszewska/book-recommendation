# Book recommendations

## Describtion:
The theme of our project was the construction of a book recommendation system. The end result is a simple server that allows you to query the API with a request for access to the recommendations of books that provide book or user input from the database.

## Data:
The data needed to implement the project were downloaded from the Goodreads database : https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home

## The following files were used in the project:
- goodreads_books.json.gz
- goodreads_interactions.csv
- goodreads_book_genres_initial.json.gz
- goodreads_book_genres_initial.json.gz
- goodreads_book_series.initial.json.gz

## The following methods were used in the project:
- Demographic filtering
- Content-based filtering
- Collaborative filtering

## Run example
The first step is to download the project and install the appropriate libraries in it. Then, download the files listed above from the Goodreads database and place them in the project in the "data" folder.
Then run: create_content_base_set.py and create_collaborative_set.py in order to properly prepare the data.
When the appropriate files are created, you can start server.py and check sample endpoints.


