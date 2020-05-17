from surprise import SVD, Reader, Dataset
from surprise.model_selection import cross_validate
import pandas as pd

# COLLABORATIVE FILTERING

reader = Reader()
merged_set = pd.read_csv('./data/merged_books_set')
merged_set.head()

data = Dataset.load_from_df(merged_set[['user_id', 'book_id', 'rating']], reader)
books_ids = merged_set['book_id'].tolist()
books_ids = list(dict.fromkeys(books_ids))

svd = SVD()
cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

train_set = data.build_full_trainset()
svd.fit(train_set)


def predict_rating(user, book_id):
    return svd.predict(user, book_id, 3)


def get_ids_of_recommended_books(user):
    all_predictions = []
    list_of_predicted_ratings = []
    print('books ids', books_ids)

    for book_id in books_ids:
        new_prediction = predict_rating(user, book_id)
        all_predictions.append({'iid': new_prediction.iid, 'est': round(new_prediction.est, 6)})
        list_of_predicted_ratings.append(round(new_prediction.est, 6))

    sr = pd.Series(list_of_predicted_ratings)
    result = sr.nlargest(n=5)
    max_values = result.tolist()

    recommended_books = []
    for value in max_values:
        for i, obj in enumerate(all_predictions):
            if obj['est'] == value:
                recommended_books.append(obj['iid'])
                break

    return recommended_books


def get_recommended_books(user):
    ids_od_recommended_books = get_ids_of_recommended_books(user)
    ids_od_recommended_books = list(dict.fromkeys(ids_od_recommended_books))
    print('ids_od_recommended_books', ids_od_recommended_books, 'user', user)
    rows = []
    for book_id in ids_od_recommended_books:
        row = merged_set.loc[merged_set['book_id'] == book_id]
        rows.append(row.iloc[0])
        # rows.append(row)
    print('rows', rows)


user = 395
get_recommended_books(user)
