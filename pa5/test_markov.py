'''
CAPP 30122: Test code for Speaker Attribution (Markov Model) assignment

Anne Rogers, Lamont Samuels
January 2019
'''

# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg= missing-docstring, line-too-long, too-many-locals
# pylint: disable-msg= too-many-locals

import os
import sys
import pytest

import markov

# Get the name of the directory that holds the grading code.
BASE_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(BASE_DIR, "speeches")

MAX_TIME = 120
EPSILON = 0.00001

TEST_DATA = [
    
    # 0
    # "bush1+2.txt" -> speaker1 file
    # "kerry1+2.txt" -> speaker2 file
    # ""bush-kerry3/BUSH-0.txt" -> unidentified speaker file
    # 2 -> K value
    # "A" -> This what your code should determine who the speark really is
    # (-2.1670591295191572, -2.2363636778055525) -> expected probabilites
    ("bush1+2.txt",
     "kerry1+2.txt", "bush-kerry3/BUSH-0.txt", 2,
     "A", (-2.1670591295191572, -2.2363636778055525)),

    # 1
    # "bush1+2.txt" -> speaker1 file
    # "kerry1+2.txt" -> speaker2 file
    # "bush-kerry3/KERRY-0.txt" -> unidentified speaker file
    # 2 -> K value
    # "B" -> This what your code should determine who the speark really is
    # (-2.250501358542073, -2.151522255004497) -> expected probabilites
    ("bush1+2.txt",
     "kerry1+2.txt", "bush-kerry3/KERRY-0.txt", 2,
     "B", (-2.250501358542073, -2.151522255004497)),

    # 2
    # "bush1+2.txt" -> speaker1 file
    # "kerry1+2.txt" -> speaker2 file
    # "bush-kerry3/BUSH-10.txt" -> unidentified speaker file
    # 1 -> K value
    # "A" -> This what your code should determine who the speark really is
    # (-2.4587597756771893, -2.4817352688426397) -> expected probabilites
    ("bush1+2.txt",
     "kerry1+2.txt", "bush-kerry3/BUSH-10.txt", 1,
     "A", (-2.4587597756771893, -2.4817352688426397)),

    # 3
    # "obama1+2.txt" -> speaker1 file
    # "mccain1+2.txt" -> speaker2 file
    # "obama-mccain3/MCCAIN-5.txt" -> unidentified speaker file
    # 2 -> K value
    # "A" -> This what your code should determine who the speark really is
    # (-1.695522966555955, -1.7481812967778005) -> expected probabilites
    ("obama1+2.txt",
     "mccain1+2.txt", "obama-mccain3/MCCAIN-5.txt", 2,
     "A", (-1.695522966555955, -1.7481812967778005)),

    # 4
    # "obama1+2.txt" -> speaker1 file
    # "mccain1+2.txt" -> speaker2 file
    # "obama-mccain3/OBAMA-15.txt" -> unidentified speaker file
    # 3 -> K value
    # "A" -> This what your code should determine who the speark really is
    # (-2.138910249777975, -2.3049185686282305) -> expected probabilites
    ("obama1+2.txt",
     "mccain1+2.txt", "obama-mccain3/OBAMA-15.txt", 3,
     "A", (-2.138910249777975, -2.3049185686282305))]

################## Speaker Tests ##################
def run_test(test_num):
    '''
    Run a specific test.
    '''

    def within(x, y):
        return abs(x - y) <= EPSILON

    def open_file(filename):
        contents = []
        if not os.path.isfile(filename):
            print("Bad file name:" + filename)
            sys.exit(0)
        with open(filename, "r") as file:
            contents = file.read()
        return contents

    # Retrieve test data
    speaker1_file, speaker2_file, unid_speaker_file, k, expected_speaker, expected_probs = TEST_DATA[test_num]
    speaker1_file = os.path.join(TEST_DATA_DIR, speaker1_file)
    speaker2_file = os.path.join(TEST_DATA_DIR, speaker2_file)
    unid_speaker_file = os.path.join(TEST_DATA_DIR, unid_speaker_file)

    speaker1 = open_file(speaker1_file)
    speaker2 = open_file(speaker2_file)
    unid_speaker = open_file(unid_speaker_file)

    actual = markov.identify_speaker(speaker1, speaker2, unid_speaker, k)

    #Check to make sure a tuple was returned by identify_speaker
    if not isinstance(actual, tuple):
        s = "Actual value returned from identify_speaker must be a tuple"
        pytest.fail(s)

    #Check to make sure three items were retrned by identify_speaker
    if len(actual) != 3:
        s = ("Actual value returned from identify_speaker must be a "
             "tuple of three components")
        pytest.fail(s)

    (prob_a, prob_b, got_speaker) = actual

    # Check to to see if the speaker returned by identify_speaker
    # matches the expected speaker

    if  got_speaker != expected_speaker:
        s = ("actual speaker ({got_speaker}) and expected speaker "
             "({expected_speaker}) values do not match")
        pytest.fail(s.format())

    # Check to to see if the probabilities returned by identify_speaker
    # matches the expected probabilities

    if not within(prob_a, expected_probs[0]):
        s = ("actual speaker probability A ({}) and expected probability "
             "({}) values do not match")
        pytest.fail(s.format(prob_a, expected_probs[0]))

    if not within(prob_b, expected_probs[1]):
        s = ("actual speaker probability A ({}) and expected probability "
             " ({}) values do not match")
        pytest.fail(s.format(prob_b, expected_probs[1]))

# If you are trying to understand these tests then please see the TEST_DATA
# variable above.
def test_0():
    run_test(0)

def test_1():
    run_test(1)

def test_2():
    run_test(2)

def test_3():
    run_test(3)

def test_4():
    run_test(4)
