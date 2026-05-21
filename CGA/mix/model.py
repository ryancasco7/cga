import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

data = {
    "Written Communication": [5, 3, 1, 2, 4],
    "Verbal Communication": [5, 3, 2, 1, 4],
    "Problem Solving": [4, 2, 1, 5, 3],
    "Teamwork": [3, 4, 5, 2, 1],
    "Analytical Ability": [5, 1, 2, 4, 3],
    "Creative Thinking": [1, 5, 4, 2, 3],
    "Numeracy": [5, 2, 1, 4, 3],
    "Leadership": [4, 5, 1, 2, 3],
    "Commercial Awareness": [4, 1, 3, 2, 5],
    "Decision Making": [5, 3, 1, 4, 2],
    "Track": ["ACADEMIC", "TVL", "ARTS AND DESIGN", "SPORTS", "ACADEMIC"]
}

df = pd.DataFrame(data)

X = df.drop("Track", axis=1)
y = df["Track"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

joblib.dump(clf, 'track_classifier.pkl')
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
