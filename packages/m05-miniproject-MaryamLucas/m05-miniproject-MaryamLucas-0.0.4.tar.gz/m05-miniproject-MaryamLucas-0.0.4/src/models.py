##### M05: MINI-PROYECTC / MAIN CODE #####

## Initialization components
# Import necessary libraries
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

# Function: linear model
def linear_model(X_train, X_test, y_train, y_test):
      # Create a Linear regressor
      lm = LinearRegression()
      # Train the model using the training sets 
      lm.fit(X_train, y_train)
      # Model prediction on train data
      y_pred = lm.predict(X_train)
      # Predicting Test data with the model
      y_test_pred = lm.predict(X_test)
      return y_test_pred, y_test


# Function: tree model
def tree_model(X_train, X_test, y_train, y_test):
      # Create a Linear regressor
      model = DecisionTreeRegressor()
      # Train the model using the training sets 
      model.fit(X_train, y_train)
      # Model prediction on train data
      y_pred = model.predict(X_train)
      # Predicting Test data with the model
      y_test_pred = model.predict(X_test)
      return y_test_pred, y_test
