from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rapidoml",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn",
        "tensorflow",
        "keras",
        "xgboost",
        "lightgbm",
        "catboost"
    ],
    author='Fabio Carvalho',
    author_email='hipnologo@gmail.com',
    license='Apache License, Version 2.0',
    description="RapidoML is a simple Automated Machine Learning (AutoML) library",
    url="https://github.com/hipnologo/rapidoml",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
