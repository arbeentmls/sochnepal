from sklearn.linear_model import LogisticRegression as _LR


class CustomToxicityClassifier:
    """Custom binary classification model for toxicity detection"""

    def __init__(self, **kwargs):
        self._classifier = _LR(**kwargs)

    def fit(self, X, y):
        return self._classifier.fit(X, y)

    def predict_proba(self, X):
        return self._classifier.predict_proba(X)

    def score(self, X, y):
        return self._classifier.score(X, y)
