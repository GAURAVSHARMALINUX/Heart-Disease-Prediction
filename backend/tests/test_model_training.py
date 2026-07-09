import numpy as np
from sklearn.linear_model import LogisticRegression

def test_model_training_and_prediction():
    X = np.random.rand(20, 5)
    y = np.random.randint(0, 2, 20)

    model = LogisticRegression()
    model.fit(X, y)

    preds = model.predict(X)
    assert len(preds) == len(y)
