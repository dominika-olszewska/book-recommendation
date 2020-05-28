import fetch as fetch_f
import content_based_filtering as content_f
import demographic_filtering as demographic_f
import collaborative_filtering as collaborative_f

from flask import Flask, jsonify

app = Flask(__name__)


# Getting random book from the set
# Example: http://127.0.0.1:5000/random
@app.route('/random/', methods=['GET'])
def random():
    book = fetch_f.get_random_book()
    return book.to_json(orient='records')


# Getting book by ID
# Example: http://127.0.0.1:5000/bookById/36067728
@app.route('/bookById/<int:id>', methods=['GET'])
def bookById(id):
    book = fetch_f.getBookByID(id)
    return book.to_json(orient='records')


# Getting book by title
# Example: http://127.0.0.1:5000/bookByTitle/Anthropology of an American Girl
@app.route('/bookByTitle/<string:title>', methods=['GET'])
def bookByTitle(title):
    book = fetch_f.getBookByTitle(title)
    return book.to_json(orient='records')


# Getting book by author
# Example: http://127.0.0.1:5000/booksByAuthor/Hilary Thayer Hamann
@app.route('/booksByAuthor/<string:author>', methods=['GET'])
def booksByAuthor(author):
    books = fetch_f.getBooksByAuthor(author)
    return books.to_json(orient='records')


# Demographic filtering
# Example:  http://127.0.0.1:5000/top
@app.route('/top/', methods=['GET'])
def demographic_filtering():
    topBooks = demographic_f.getTopBooks()
    return topBooks.to_json(orient='records')


# Content based filtering
# Example:  http://127.0.0.1:5000/similarTo/Anthropology of an American Girl
@app.route('/similarTo/<string:title>', methods=['GET'])
def content_based_filtering(title):
    similarBooks = content_f.get_recommendations(title)
    return similarBooks.to_json(orient='records')


# Collaborative filtering
# Example:  http://127.0.0.1:5000/suggestionFor/395
@app.route('/suggestionFor/<int:user_id>', methods=['GET'])
def collaborative_filtering(user_id):
    suggestedBooks = collaborative_f.get_recommended_books(user_id)
    return suggestedBooks.to_json(orient='records')


if __name__ == '__main__':
    app.run(debug=True)
