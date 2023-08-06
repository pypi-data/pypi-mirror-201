# RapidoML: Automated Machine Learning Made Simple

RapidoML is an easy-to-use Python library that automates the process of building and optimizing machine learning models. It simplifies feature selection, hyperparameter tuning, and model selection, making it perfect for quickly prototyping and testing models. RapidoML relies on popular dependencies like scikit-learn, NumPy, TensorFlow, Keras, XGBoost, LightGBM, and CatBoost.

[![License: Apache License 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Forks](https://img.shields.io/github/forks/hipnologo/RapidoML)](https://github.com/hipnologo/RapidoML/network/members)
[![Stars](https://img.shields.io/github/stars/hipnologo/RapidoML)](https://github.com/hipnologo/RapidoML/stargazers)
[![Issues](https://img.shields.io/github/issues/hipnologo/RapidoML)](https://github.com/hipnologo/RapidoML/issues)


## Installation

You can install RapidoML using `pip`:

```bash
pip install RapidoML
```


This will install the required dependencies along with the RapidoML library.

## Quickstart

First, import the required functions from the library:

```python
import rapidomL
from rapidoml.datasets import sample_datasets
``` 

Load a sample dataset, such as Iris, Titanic, or others, and split it into training and testing sets with a 70/30 ratio. The function `sample_datasets` also performs preprocessing, cleaning, and normalization.

```python
df_train, df_test = sample_datasets('iris')
```

Create an instance of the `AutoML` class and train the model using the training dataset. If you want to specify the model to use, you can pass it as an argument, for example: `model='XGBClassifier'`. Otherwise, RapidoML will automatically pick the best model for the given dataset.

```python
automl = RapidoML.AutoML()
automl.train(df_train)
```

Evaluate the model using the testing dataset. This will return a dictionary containing evaluation metrics for the trained model, such as accuracy, precision, recall, and F1 score for classification tasks, or R2, MSE, and MAE for regression tasks.

```python
metrics = RapidoML.evaluate(automl, df_test, model_type='classifier')
print(metrics)
```

Finally, save the trained model to a pickle file for future use.

```python
automl.save()
```

## Custom Datasets
If you want to use your own dataset, follow these steps:

1. Load your dataset using your preferred method (e.g., `pandas.read_csv`).
2. Preprocess your dataset (cleaning, normalization, etc.).
3. Split the dataset into training and testing sets (e.g., using `train_test_split` from `sklearn.model_selection`).
4. Pass the training dataset to the `train` function of the `AutoML` instance.
5. Evaluate and save the model as described in the Quickstart example above.

## Supported Models
RapidoML supports various models, including:

- DeepLearningClassifier and DeepLearningRegressor
- XGBClassifier and XGBRegressor
- LGBMClassifier and LGBMRegressor
- CatBoostClassifier and CatBoostRegressor

You can easily extend the library by adding more models to the `models.py` file.

## Contributing
If you'd like to contribute to RapidoML, feel free to submit pull requests, report issues, or suggest new features. Your feedback is highly appreciated!

### Support
If you have any questions or need help using RapidoML, please post a question or [open an issue](https://github.com/hipnologo/RapidoML/issues) on GitHub.