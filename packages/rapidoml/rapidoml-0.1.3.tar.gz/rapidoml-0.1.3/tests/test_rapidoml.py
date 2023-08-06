import unittest
import pandas as pd
from sklearn.metrics import accuracy_score

from rapidoml import AutoML
from rapidoml.datasets import load_dataset, preprocess_data


class TestRapidoML(unittest.TestCase):

    def test_load_dataset(self):
        X, y = load_dataset('iris.csv', target_column='species')
        self.assertIsInstance(X, pd.DataFrame)
        self.assertIsInstance(y, pd.Series)

    def test_automl_iris(self):
        X, y = load_dataset('iris.csv', target_column='species')
        X_train, X_test, y_train, y_test = preprocess_data(X, y, test_size=0.3)

        automl = AutoML()
        automl.train(X_train, y_train, model='XGBClassifier')
        y_pred = automl.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        self.assertGreater(accuracy, 0.8)
