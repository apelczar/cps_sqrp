'''
Test code for building decision trees.
'''

import json
import pandas as pd
import pytest

from decision_tree import go

TEST_FILES = [("ex.json", "example_from_class"),
              ("tennis.json", "tennis_example"),
              ("pima.json", "pima_data"),
              ("all_no.json", "all_no"),
              ("unseen.json", "unseen_attribute_value")]

DATA_DIR = "./data/"

def run_test(test_file, desc):
    '''
    Do a single test with test_file.
    '''
    try:
        f = open(test_file)
        test_info = json.load(f)
    except IOError:
        pytest.fail(test_file + " not found. Have you downloaded the data?")

    actual = go("./" + test_info["training_filename"],
                "./" + test_info["testing_filename"])

    expected = test_info["results"]

    s = "Test " + desc + "\n"

    if isinstance(actual, (list, pd.Series)):
        if isinstance(actual, pd.Series):
            actual = list(actual)
        if actual != expected:
            if len(actual) != len(expected):
                s = s + "Length of actual {} != length of expected {}.\n"
                s = s.format(len(actual), len(expected))
                pytest.fail(s)
            else:
                for i, aval in enumerate(actual):
                    if isinstance(aval, str):
                        if aval != expected[i]:
                            s = s + "Actual {} and Expected {} differ at {}"
                            s = s.format(aval, expected[i], i)
                            pytest.fail(s)
                    else:
                        s = s + "Predicted values should be type str, got {}.\n"
                        s = s.format(type(aval))
                        s = s + "Hint -- load your CSV data in as strings."
                        pytest.fail(s)
    else:
        s = s + "Expected list or series. Got {}"
        s = s.format(type(actual))
        pytest.fail(s)

@pytest.mark.parametrize("config_file,desc", TEST_FILES)
def test_go(config_file, desc):
    '''
    Test harness.
    '''
    run_test(DATA_DIR + config_file, desc)
