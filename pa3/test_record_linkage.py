'''
Test code for record linkage assignment
'''

# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg= broad-except

import csv
import pytest
import record_linkage as rl

def find_bad_entries(actual, expected):
    '''
    Find entries in actual and expected that do not match
    '''

    s = ""
    count = 0
    for key in set(expected).union(actual):
        if key not in actual:
            if count < 10:
                s = s + "  Missing entry for {}".format(key)
            count += 1
        elif key not in expected:
            if count < 10:
                s = s + "  Unexpected entry for {}".format(key)
            count += 1
        elif actual[key] != expected[key]:
            if count < 10:
                msg = ("  Actual value {} for {} does not"
                       "  match the expected value {}.")
                msg = msg.format(actual[key], key, expected[key])
                s = s + msg
            count += 1

    if s:
        msg = "Issues with {} entries.  Here are some sample issues:"
        msg = msg.format(count) + s
        pytest.fail(msg)



def helper(output_prefix, mu, lambda_, block_on_city):
    '''
    Test helper function
    '''

    expected_filename = output_prefix + "_expected.csv"
    try:
        expected = [row for row in csv.reader(open(expected_filename))]
    except IOError:
        msg = "Could not open expected file: {}"
        msg = msg.format(expected_filename)
        pytest.fail(msg)

    actual_filename = output_prefix + "_actual.csv"

    try:
        rl.find_matches(actual_filename, mu, lambda_,
                        block_on_city=block_on_city)
        actual = [[x.strip() for x in row] for row \
                      in csv.reader(open(actual_filename))]
    except IOError:
        msg = "Could not open actual file: {}"
        msg = msg.format(actual_filename)
        pytest.fail(msg)
    except Exception as e:
        msg = "Exception thrown: {}".format(e)
        pytest.fail(msg)

    if len(actual) != len(expected):
        msg = ("Length of actual result ({})\n"
               "does not match the expected length ({})")
        msg = msg.format(len(actual), len(expected))
        pytest.fail(msg)

    if expected == actual:
        return

    if not all([len(row) == 3 for row in actual]):
        msg = ("Actual result has the wrong format.\n"
               "Expected rows with: zagat index, fordor index, label\n")
        pytest.fail(msg)

    actual = {(z, f):label for z, f, label in actual}
    expected = {(z, f):label for z, f, label in expected}

    if expected == actual:
        return

    find_bad_entries(actual, expected)


def test_find_match_1():
    ''' Basic test '''
    helper("output/basic", 0.005, 0.005, False)

def test_find_match_2():
    ''' Set parameters to push a tuple from match to possible '''
    helper("output/push_match_to_possible", 0.0, 0.01, False)

def test_find_match_3():
    ''' Set parameters to push a tuple from unmatch to possible '''
    helper("output/pickup_unmatch_from_possible", 0.0, 0.03, False)

def test_find_match_4():
    ''' Test cross over between match range and unmatch range '''
    helper("output/cross_over", 0.005, 0.05, False)

def test_find_match_5():
    ''' Test blocking '''
    helper("output/basic_blocking", 0.005, 0.005, True)
