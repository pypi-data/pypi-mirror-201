import unittest
import pandas as pd
from rapidoml.datasets import sample_datasets
from rapidoml.preprocessing import preprocess_data
from sklearn.datasets import load_iris, load_digits

class TestSampleDatasets(unittest.TestCase):
    def test_iris_dataset(self):
        X_train, X_test, y_train, y_test = sample_datasets('iris')
        iris = load_iris()
        df_train = pd.DataFrame(X_train, columns=iris.feature_names)
        df_test = pd.DataFrame(X_test, columns=iris.feature_names)
        df_train['species'] = y_train
        df_test['species'] = y_test

        df_processed = preprocess_data(df_train, categorical_columns=['species'], numerical_columns=iris.feature_names)
        self.assertEqual(df_processed['species'].nunique(), 3)

    def test_digits_dataset(self):
        X_train, X_test, y_train, y_test = sample_datasets('digits')
        digits = load_digits()
        df_train = pd.DataFrame(X_train, columns=[f"pixel_{i}" for i in range(X_train.shape[1])])
        df_test = pd.DataFrame(X_test, columns=[f"pixel_{i}" for i in range(X_train.shape[1])])
        df_train['target'] = y_train
        df_test['target'] = y_test

        df_processed = preprocess_data(df_train, numerical_columns=[f"pixel_{i}" for i in range(X_train.shape[1])])
        self.assertAlmostEqual(df_processed.mean().sum(), 0.0, delta=1e-6)


if __name__ == '__main__':
    unittest.main()
