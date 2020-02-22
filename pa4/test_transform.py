'''
Test code for Pima Indians Diabetes Data cleaning task
'''

import pandas as pd
import pytest
import os

# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable= too-many-boolean-expressions

import transform

@pytest.fixture(autouse=True)
def clean_upfiles():
    # do the tests and then cleanup
    yield

    try:
        os.remove("pima-testing.csv")
    except FileNotFoundError:
        pass

    try:
        os.remove("pima-training.csv")
    except FileNotFoundError:
        pass

def find_diff_helper(col, max_rows, df, df_expected):
    '''
    Compare a column in two data frames.  If they are different, find
    and report up to max rows in that differ in that column.

    Inputs:
      col (string): name of the column to check
      max_rows (int): maximum number of different rows to find
      df, df_expected: data frames
    '''
    s = ""
    num_rows = 0
    for i in df_expected.index:
        a = df[col][i]
        e = df_expected[col][i]
        if pd.notnull(a) and isinstance(a, float) and \
           pd.notnull(e) and isinstance(e, float):
            if  a != pytest.approx(e):
                s += "    Row {}: {} != {}\n".format(i, a, e)
                num_rows += 1
                if num_rows == max_rows:
                    break
        elif (a != e and pd.notnull(a) and pd.notnull(e)) or \
             (pd.isnull(a) and pd.notnull(e)) or \
             (pd.notnull(a) and pd.isnull(e)):
            s += "    Row {}: {} != {}\n".format(i, a, e)
            num_rows += 1
            if num_rows == max_rows:
                break
    if s:
        s = "\n  {} error:\n".format(col) + s
        pytest.fail(s)


def check_all_helper(df, df_expected):
    '''
    Compare two data frames. If they are different find and report up
    to three rows in which they differ.

    Inputs:
      df, df_expected: data frames
    '''

    if df_expected is None and df is None:
        return

    if df is None:
        pytest.fail("Got unexpected None for dataframe")

    if set(df.columns) != set(df_expected.columns):
        msg = "Actual columns: {} and\nExpected columns: {}\ndo not match"
        msg = msg.format(df.columns, df_expected.columns)
        pytest.fail(msg)

    if df.shape != df_expected.shape:
        msg = "Actual shape {} and\nExpected shape: {}\ndo not match"
        msg = msg.format(df.shape, df_expected.shape)
        pytest.fail(msg)

    if df.sort_index(axis=1).equals(df_expected.sort_index(axis=1)):
        return

    for col in df_expected.columns:
        find_diff_helper(col, 3, df, df_expected)

def compare_files(actual_filename, expected_filename):
    '''

    Compare two CSV files as dataframes. If they are different find
    and report up to three rows in which they differ.

    Inputs:
      df: actual data frames
      output_pickle_filename: name of pickle file with expected
        results or None
    '''

    err_msg = "Could not open/read file: {}"
    try:
        df_actual = pd.read_csv(actual_filename)
    except IOError:
        msg = "\nYour data cleaning task should have produced this file."
        pytest.fail(err_msg.format(actual_filename)
                    + msg)

    try:
        df_expected = pd.read_csv(expected_filename)
    except IOError:
        pytest.fail(err_msg.format(expected_filename)
                    + "\nDid you remember to run data/get_files.sh?")

    check_all_helper(df_actual, df_expected)

def test_clean():
    '''
    Test the code for cleaning the Pima Indians Diabetes data.
    '''

    actual_training_filename = "pima-training.csv"
    actual_testing_filename = "pima-testing.csv"

    transform.clean("data/pima-indians-diabetes.csv",
                    actual_training_filename,
                    actual_testing_filename,
                    1234)

    compare_files(actual_training_filename, "data/pima-training-expected.csv")
    compare_files(actual_testing_filename, "data/pima-testing-expected.csv")
