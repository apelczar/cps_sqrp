'''
PA #4: Clean Pima Indians Diabetes Data

Your name
'''

import sys

import pandas as pd
from sklearn.model_selection import train_test_split

BOUNDS = {'Number of pregnancies': ([0, 2, 6, float("inf")],
                                    ["low", "medium", "high"]),
          'Plasma glucose level': ([0.1, 95, 141, float("inf")],
                                   ["low", "medium", "high"]),
          'Diastolic Blood Pressure': ([0.1, 80, 90, float("inf")],
                                       ["normal", "pre-hypertension",
                                        "high"]),
          'Body Mass Index': ([0.1, 18.5, 25.1, 30.1, float("inf")],
                              ["low", "healthy", "obese",
                               "severely-obese"]),
          'Diabetes Pedigree Function': ([0.001, 0.42, 0.82, float("inf")],
                                         ["low", "medium", "high"]),
          'Age (in years)': ([0.1, 41, 60, float("inf")],
                             ["r1", "r2", "r3"])}

def clean(raw_filename, training_filename, testing_filename, seed):
    '''
    Do the work of cleaning the Pima Indians Diabetes dataset.

    Inputs:
      raw_filename (string): name of the file with the original data
      training_filename (string): name of the file for the
        (cleaned) training data
      testing_filename (string): name of the file for the
        (cleaned) testing data
      seed: seed for splitting the original data into testing and training sets.
    '''

    # replace pass with your code and remove this comment.
    pass

def go(args):
    '''
    Process the arguments and call clean.
    '''

    usage = ("usage: python3 {} <raw data filename> <training filename>"
             " <testing filename> [seed]")
    if len(args) < 4 or len(args) > 5:
        print(usage.format(args[0]))
        sys.exit(1)

    try:
        if len(args) == 4:
            seed = None
        else:
            seed = int(args[4])
    except ValueError:
        print(usage)
        print("The seed must be an integer")
        sys.exit(1)

    clean(args[1], args[2], args[3], seed)

if __name__ == "__main__":
    go(sys.argv)
