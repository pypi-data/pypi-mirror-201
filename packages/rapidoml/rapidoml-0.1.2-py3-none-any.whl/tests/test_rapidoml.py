import unittest
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from rapidoml import AutoML
from rapidoml.datasets import sample_datasets
from rapidoml.preprocessing import preprocess_data


class TestRapidoML(unittest.TestCase):

    def test_sample_datasets(self):
        df_train, df_test = sample_datasets('iris')
        self.assertIsInstance(df_train, pd.DataFrame)
        self.assertIsInstance(df_test, pd.DataFrame)

    def test_automl_iris(self):
        df_train, df_test = sample_datasets('iris')
        X_train, X_test, y_train, y_test = preprocess_data(df_train, categorical_columns=['target'], numerical_columns=df_train.columns[:-1], test_size=0.3)

        automl = AutoML()
        automl.train(X_train, y_train, model='XGBClassifier')
        y_pred = automl.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        self.assertGreater(accuracy, 0.8)

