import unittest
import pandas as pd
from rapidoml.datasets import sample_datasets
from rapidoml.preprocessing import preprocess_data


class TestSampleDatasets(unittest.TestCase):
    def test_iris_dataset(self):
        X_train, X_test, y_train, y_test = sample_datasets('iris')
        df_train = pd.DataFrame(X_train, columns=iris.feature_names)
        df_test = pd.DataFrame(X_test, columns=iris.feature_names)
        df_train['target'] = y_train
        df_test['target'] = y_test

        df_processed = preprocess_data(df_train, categorical_columns=['species'], numerical_columns=iris.feature_names)
        self.assertEqual(df_processed['species'].nunique(), 3)

    def test_digits_dataset(self):
        X_train, X_test, y_train, y_test = sample_datasets('digits')
        df_train = pd.DataFrame(X_train)
        df_test = pd.DataFrame(X_test)
        df_train['target'] = y_train
        df_test['target'] = y_test

        df_processed = preprocess_data(df_train, numerical_columns=df_train.columns[:-1])
        self.assertAlmostEqual(df_processed.mean().sum(), 0.0, delta=1e-6)


if __name__ == '__main__':
    unittest.main()
