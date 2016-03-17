from preprocess_data import load_session, prepare_feats_labels, split_to_training_and_test
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from sklearn import metrics
import numpy as np

session = load_session('f_mupssan20140901.F:FESXU4.pkl')
feats, labels = prepare_feats_labels(session)
feats_tr, feats_tst, labels_tr, labels_tst = split_to_training_and_test(feats, labels)


# Create linear regression object
#regr = linear_model.PassiveAggressiveRegressor()  # 0.064
#regr = linear_model.BayesianRidge()  # 0.747
regr = linear_model.OrthogonalMatchingPursuit()  # 0.75
#regr = linear_model.Lars()  # 0.0
#regr = linear_model.Lasso()  # 0.60
#regr = linear_model.Ridge()  # 0.74
#regr = linear_model.LinearRegression()  # 0.74
#regr = linear_model.LogisticRegression()  # 0.09

# Train the model using the training sets
regr.fit(feats_tr, labels_tr)

predictions = regr.predict(feats_tst)
# price is integer, predictions float, round to int since sklearn complains about mixing continuous and multiclass
predictions = np.rint(predictions)
acc = metrics.accuracy_score(labels_tst, predictions)
print '---> accuracy_score:', acc
