"""
    Classify customer reviews (Supervised learning)
"""

import sys
import os
import pickle
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from notebooks.preprocessing import load_and_preprocess_data, split_data

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

data = load_and_preprocess_data()
X_train, X_test, y_train, y_test, csv_data = split_data(data)

# ### Naive Bayes
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)

y_pred_train = nb_model.predict(X_train)
y_pred = nb_model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))


# ### XGBoost
xgb = XGBClassifier(eval_metric='mlogloss')

param_grid = {
    'n_estimators': [100, 200, 500],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.3],
}

# Find the best hyper params
grid_search = GridSearchCV(
    estimator=xgb,
    param_grid=param_grid,
    scoring='accuracy',
    cv=5,
    verbose=0,
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

print("Best params", grid_search.best_params_)
best_model = grid_search.best_estimator_

y_pred = best_model.predict(X_test)

print("Accuracy Score:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))


# ## Save model
with open("../models/xgb_model.pkl", "wb") as f:
    pickle.dump(best_model, f)
