from preprocess_data import load_session, prepare_feats_labels, split_to_training_and_test
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from sklearn import metrics
import numpy as np

session = load_session('f_mupssan20140901.F:FESXU4.pkl')
feats, labels = prepare_feats_labels(session, window=5, label_after=100, label_column=4, overlap=0)
feats_tr, feats_tst, labels_tr, labels_tst = split_to_training_and_test(feats, labels)


# Create linear regression object
#regr = linear_model.PassiveAggressiveRegressor()  # 0.064 window=10, label_after=10
#regr = linear_model.BayesianRidge()  # 0.747 window=10, label_after=10
# OrthogonalMatchingPursuit
# 0.75 window=10, label_after=10
# 0.45  window=5, label_after=100
regr = linear_model.OrthogonalMatchingPursuit()
#regr = linear_model.Lars()  # 0.0 window=10, label_after=10
#regr = linear_model.Lasso()  # 0.60 window=10, label_after=10
#regr = linear_model.Ridge()  # 0.74 window=10, label_after=10
#regr = linear_model.LinearRegression()  # 0.74 window=10, label_after=10
#regr = linear_model.LogisticRegression()  # 0.09 window=10, label_after=10

# from sklearn import svm
# regr = svm.SVC()  # 0.09 window=10, label_after=10

# tree.DecisionTreeClassifier
# 0.64 window=10, label_after=10
# 0.62 window=10, label_after=100
# 0.26 window=100, label_after=100
# 0.73 window=5, label_after=100
#from sklearn import tree
#regr = tree.DecisionTreeClassifier()

# Train the model using the training sets
regr.fit(feats_tr, labels_tr)

predictions = regr.predict(feats_tst)
# price is integer, predictions float, round to int since sklearn complains about mixing continuous and multiclass
predictions = np.rint(predictions)
acc = metrics.accuracy_score(labels_tst, predictions)
print '---> accuracy_score:', acc
