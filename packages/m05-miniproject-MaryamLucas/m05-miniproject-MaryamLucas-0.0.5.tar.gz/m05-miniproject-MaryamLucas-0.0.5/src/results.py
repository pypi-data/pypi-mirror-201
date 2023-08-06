##### M05: MINI-PROYECTC / MAIN CODE #####

## Initialization components
# Import necessary libraries
import numpy as np
from sklearn import metrics

# Function: linear model
def indices(y_test, y_test_pred):

      # Model Evaluation: index
      acc_linreg = metrics.r2_score(y_test, y_test_pred)
      MAE = metrics.mean_absolute_error(y_test, y_test_pred)
      MSE = metrics.mean_squared_error(y_test, y_test_pred)
      RMSE = np.sqrt(metrics.mean_squared_error(y_test, y_test_pred))
      print('MAE:', MAE)
      print('R^2:', acc_linreg)
      print('MSE:', MSE)
      print('RMSE:', RMSE)
      
      return MAE, MSE, RMSE, acc_linreg

