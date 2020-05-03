from surprise import SVD
from surprise.model_selection import cross_validate
import app

# COLLABORATIVE FILTERING

# The lower the RMSE, the better the performance
svd = SVD()
cross_validate(svd, app.data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

trainSet = app.data.build_full_trainset()
svd.fit(trainSet)

USER_RATINGS = app.ratings_data[app.ratings_data['user_id'] == 1]

print('USER_RATINGS', USER_RATINGS)

prediction = svd.predict(1, 302, 3)

print('prediction', prediction)