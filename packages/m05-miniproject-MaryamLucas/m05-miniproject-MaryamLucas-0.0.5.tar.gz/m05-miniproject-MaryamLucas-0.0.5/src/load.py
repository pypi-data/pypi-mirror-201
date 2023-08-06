##### M05: MINI-PROYECTC / MAIN CODE #####

## Initialization components
# Import necessary libraries
import os
import argparse 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler


# Function: dataset boston open and pre-processing
def data_boston():
      
      # Obtention of path dir and open data
      current_directory = os.path.dirname(__file__)
      parent_directory = os.path.split(current_directory)[0]
      data_boston_original = pd.read_csv(parent_directory+'/src/Datasets/boston_data/housing.data', header=None)
      
      # Ordering data in columns and adding head
      data_boston = data_boston_original[0].str.split(expand=True)
      data_boston_columns = np.array(['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'PRICE'])
      data_boston.columns = data_boston_columns

      # Distinction variable/independent variables
      X = data_boston.drop(['PRICE'], axis = 1)
      y = data_boston['PRICE']

      # Preprocessing data min-max scaling
      minmax = MinMaxScaler()
      data_boston[data_boston.columns] = minmax.fit_transform(data_boston[data_boston.columns])
      autoscaler = StandardScaler()
      data_boston[data_boston.columns] = autoscaler.fit_transform(data_boston[data_boston.columns])

      # Splitting to training and testing data
      global X_train, X_test, y_train, y_test
      X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.5, random_state = 4)
      return X_train, X_test, y_train, y_test


# Function: dataset wine open and pre-processing
def data_whitewine():

      # Obtention of path dir and open data
      current_directory = os.path.dirname(__file__)
      parent_directory = os.path.split(current_directory)[0]
      data_ww = pd.read_csv(parent_directory+'/src/Datasets/wine_data/winequality-red.csv', header=None)
      data_ww = data_ww[0].str.split(';', expand=True)

      data_ww.columns = data_ww.iloc[0]
      data_ww = data_ww[1:]

      # Distinction variable/independent variables
      X = data_ww.drop(['"quality"'], axis = 1)
      y = data_ww['"quality"']

      # Preprocessing data min-max and standar scaling
      minmax = MinMaxScaler()
      data_ww [data_ww.columns] = minmax.fit_transform(data_ww[data_ww.columns])
      autoscaler = StandardScaler()
      data_ww[data_ww.columns] = autoscaler.fit_transform(data_ww[data_ww.columns])

      # Splitting to training and testing data
      global X_train, X_test, y_train, y_test
      X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.5, random_state = 4)
      return X_train, X_test, y_train, y_test
      
# Function: dataset wine open and pre-processing
def data_redwine():

      # Obtention of path dir and open data
      current_directory = os.path.dirname(__file__)
      parent_directory = os.path.split(current_directory)[0]
      data_rw = pd.read_csv(parent_directory+'/src/Datasets/wine_data/winequality-white.csv', header=None)
      data_rw = data_rw[0].str.split(';', expand=True)

      data_rw.columns = data_rw.iloc[0]
      data_rw = data_rw[1:]

      # Distinction variable/independent variables
      X = data_rw.drop(['"quality"'], axis = 1)
      y = data_rw['"quality"']

      # Preprocessing data min-max scaling
      minmax = MinMaxScaler()
      data_rw[data_rw.columns] = minmax.fit_transform(data_rw[data_rw.columns])
      autoscaler = StandardScaler()
      data_rw[data_rw.columns] = autoscaler.fit_transform(data_rw[data_rw.columns])

      # Splitting to training and testing data
      global X_train, X_test, y_train, y_test
      X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.5, random_state = 4)
      return X_train, X_test, y_train, y_test
