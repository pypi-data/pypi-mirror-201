##### M05: MINI-PROYECT / TESTs #####

# Import framework UT
import pytest
import pathlib as pl

# Import functions
from models import linear_model
from load import data_boston
from results import indices

# Setting a case to test the features of indices
X_train, X_test, y_train, y_test = data_boston()
y_test, y_test_pred = linear_model(X_train, X_test, y_train, y_test)
MAE, MSE, RMSE, acc_linreg = indices(y_test, y_test_pred)

# Test: features of indices
def test_output_model_format():
	# None, number, format, range
	assert (MAE is None) == False
	assert (isinstance(MAE, (int, float, complex)) and not isinstance(MAE, bool)) == True
	assert (MSE is None) == False
	assert (isinstance(MSE, (int, float, complex)) and not isinstance(MSE, bool)) == True
	assert (RMSE is None) == False
	assert (isinstance(RMSE, (int, float, complex)) and not isinstance(RMSE, bool)) == True
	assert (acc_linreg is None) == False
	assert (isinstance(acc_linreg, (int, float, complex)) and not isinstance(acc_linreg, bool)) == True
	assert (-2 <= acc_linreg <= 2) == True
	
	
