import unittest
import pandas as pd
import numpy as np
from rapidoml.preprocessing import preprocess_data

class TestPreprocessing(unittest.TestCase):
    def test_preprocess_data_categorical(self):
        data = {'category': ['A', 'B', 'A', 'C']}
        df = pd.DataFrame(data)
        df_processed = preprocess_data(df, categorical_columns=['category'])
        self.assertEqual(df_processed['category'].nunique(), 3)

    def test_preprocess_data_numerical(self):
        data = {'value': [1, 2, 3, 4, 5, 6]}
        df = pd.DataFrame(data)
        df_processed = preprocess_data(df, numerical_columns=['value'])
        self.assertAlmostEqual(np.mean(df_processed['value']), 0.0, delta=1e-6)

    def test_preprocess_data_invalid_scaling_method(self):
        data = {'value': [1, 2, 3, 4, 5, 6]}
        df = pd.DataFrame(data)
        with self.assertRaises(ValueError):
            preprocess_data(df, numerical_columns=['value'], scaling_method='unknown')

if __name__ == '__main__':
    unittest.main()
