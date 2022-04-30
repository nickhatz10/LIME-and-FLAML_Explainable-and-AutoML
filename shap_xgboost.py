# -*- coding: utf-8 -*-
"""SHAP_XGBOOST

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qkrBzJnmYxXGyDxVXIorxNJp8dAzEiR_
"""

pip install shap

from sklearn.model_selection import train_test_split
import xgboost
import shap
import numpy as np
import matplotlib.pylab as pl

# print the JS visualization code to the notebook
shap.initjs()

X,y = shap.datasets.adult()
X_display,y_display = shap.datasets.adult(display=True)

# create a train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
#  d_train = xgboost.DMatrix(X_train, label=y_train)
#  d_test = xgboost.DMatrix(X_test, label=y_test)



pip install flaml

# flaml to tune a classifiers hyperparameters

# flaml to find the most accurate classifier
from flaml import AutoML
automl = AutoML()
automl_settings = {"metric": 'accuracy', "task": 'classification', "time_budget": 120, 'estimator_list': ["xgboost"]}
#automl.fit(X_train = X_train, y_train = y_train, **automl_settings)
automl.fit(X_train, y_train, **automl_settings)
prediction = automl.predict(X_test)

automl.model

from sklearn.metrics import accuracy_score

accuracy_score(prediction, y_test)

# this takes a minute or two since we are explaining over 30 thousand samples in a model with over a thousand trees
explainer = shap.TreeExplainer(automl.model.model)
shap_values = explainer.shap_values(X_test)

print(shap_values)

shap.initjs()
shap.force_plot(explainer.expected_value, shap_values[0,:], X_display.iloc[0,:])

shap.initjs()
shap.force_plot(explainer.expected_value, shap_values[:1000,:], X_display.iloc[:1000,:])

shap.initjs()
shap.summary_plot(shap_values, X_display, plot_type="bar")