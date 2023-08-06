##### M05: MINI-PROYECT / TESTs #####

# Import framework UT
import pytest
import pathlib as pl

    
# Test: files exist in its folders
def test_exist():
	# Boston dataset
	boston_exist = pl.Path("src/Datasets/boston_data/housing.data")
	assert boston_exist.is_file() == True
	# Red Wine dataset
	wr_exist = pl.Path("src/Datasets/wine_data/winequality-red.csv")
	assert wr_exist.is_file() == True
	# White Wine dataset
	ww_exist = pl.Path("src/Datasets/wine_data/winequality-white.csv")
	assert ww_exist.is_file() == True
