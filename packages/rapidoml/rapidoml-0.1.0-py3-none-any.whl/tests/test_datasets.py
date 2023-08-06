import unittest
import pandas as pd
from rapidoml.datasets import sample_datasets

class TestSampleDatasets(unittest.TestCase):
    def test_iris_dataset(self):
        df_train, df_test = sample_datasets('iris')
        self.assertIsInstance(df_train, pd.DataFrame)
        self.assertIsInstance(df_test, pd.DataFrame)
        self.assertEqual(len(df_train.columns), len(df_test.columns))

    def test_titanic_dataset(self):
        df_train, df_test = sample_datasets('titanic')
        self.assertIsInstance(df_train, pd.DataFrame)
        self.assertIsInstance(df_test, pd.DataFrame)
        self.assertEqual(len(df_train.columns), len(df_test.columns))

    def test_unknown_dataset(self):
        with self.assertRaises(ValueError):
            sample_datasets('unknown_dataset')

if __name__ == '__main__':
    unittest.main()
