##### M05: MINI-PROYECT / TESTs #####

# Import framework UT
import pytest
import pathlib as pl

from models import linear_model
from load import data_boston

# Setting a case to test behavior of the model
X_train, X_test, y_train, y_test = data_boston()
y_test, y_test_pred = linear_model(X_train, X_test, y_train, y_test)

# Test: output of model
def test_output_model_format():
	# Empty, none, size
	assert y_test_pred.empty == False
	assert (y_test_pred is None) == False
	assert y_test_pred.size == y_test.size	
