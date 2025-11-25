import numpy as np


class CustomLogisticRegression:
    def __init__(self, learning_rate=0.01, max_iter=1000):
        self.lr = learning_rate
        self.max_iter = max_iter
        self.weights = None
        self.bias = None

    def _sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.max_iter):
            # Forward pass
            z = np.dot(X, self.weights) + self.bias
            predictions = self._sigmoid(z)

            # Compute gradients
            dw = (1 / n_samples) * np.dot(X.T, (predictions - y))
            db = (1 / n_samples) * np.sum(predictions - y)

            # Update weights
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

        return self

    def predict_proba(self, X):
        z = np.dot(X, self.weights) + self.bias
        proba = self._sigmoid(z)
        return np.vstack([1 - proba, proba]).T

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

    def score(self, X, y):
        return np.mean(self.predict(X) == y)


class CustomToxicityClassifier:
    """Custom binary classification model for toxicity detection"""

    def __init__(self, **kwargs):
        self._classifier = CustomLogisticRegression(**kwargs)

    def fit(self, X, y):
        return self._classifier.fit(X, y)

    def predict_proba(self, X):
        return self._classifier.predict_proba(X)

    def score(self, X, y):
        return self._classifier.score(X, y)
