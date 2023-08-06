##### M05: MINI-PROYECTC / MAIN CODE #####

## Initialization components
# Import necessary libraries
import argparse 
# Import function from load.py and model.py files
from load import data_boston, data_whitewine, data_redwine
from models import linear_model, tree_model
from results import indices


# Setting arguments of execution
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--database', help="Select data base.")
parser.add_argument('-m', '--model', help="Select model.")
args = parser.parse_args()


# Match the arguments with dataset and model cases
match args.database:
      case "boston":
            X_train, X_test, y_train, y_test = data_boston()
      case "redwine":
            X_train, X_test, y_train, y_test = data_redwine()
      case "whitewine":
            X_train, X_test, y_train, y_test = data_whitewine()

match args.model:
      case "linear":
            y_test, y_test_pred = linear_model(X_train, X_test, y_train, y_test)
            indices(y_test, y_test_pred)
      case "tree":
            y_test, y_test_pred = tree_model(X_train, X_test, y_train, y_test)
            indices(y_test, y_test_pred)
