import unittest
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import rapidoml
from rapidoml.datasets import sample_datasets

class TestRapidoML(unittest.TestCase):

    def test_sample_datasets(self):
        df_train, df_test = sample_datasets('iris')
        self.assertIsInstance(df_train, pd.DataFrame)
        self.assertIsInstance(df_test, pd.DataFrame)

    def test_automl_iris(self):
        df_train, df_test = sample_datasets('iris')
        X_train, y_train = df_train.drop('target', axis=1), df_train['target']
        X_test, y_test = df_test.drop('target', axis=1), df_test['target']
        
        automl = rapidoml.AutoML()
        automl.train(X_train, y_train)
        y_pred = automl.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.assertGreater(accuracy, 0.8)

    def test_automl_save_and_load(self):
        df_train, df_test = sample_datasets('iris')
        X_train, y_train = df_train.drop('target', axis=1), df_train['target']
        X_test, y_test = df_test.drop('target', axis=1), df_test['target']
        
        automl = rapidoml.AutoML()
        automl.train(X_train, y_train)
        
        automl.save("test_model.pkl")
        loaded_automl = rapidoml.AutoML.load("test_model.pkl")
        y_pred = loaded_automl.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.assertGreater(accuracy, 0.8)

if __name__ == '__main__':
    unittest.main()
