'''
Linking restaurant records in Zagat and Fodor's list using restraurant
names, cities, and street addresses.

YOUR NAME

'''
import csv
import jellyfish
import pandas as pd

import util

def find_matches(output_filename, mu, lambda_, block_on_city=False):
    '''
    Put it all together: read the data and apply the record linkage
    algorithm to classify the potential matches.

    Inputs:
      output_filename (string): the name of the output file,
      mu (float) : the maximum false positive rate,
      lambda_ (float): the maximum false negative rate,
      block_on_city (boolean): indicates whether to block on the city or not.
    '''

    # Hard-coded filename
    zagat_filename = "data/zagat.csv"
    fodors_filename = "data/fodors.csv"
    known_links_filename = "data/known_links.csv"

    ### YOUR CODE HERE

### YOUR AUXILIARY FUNCTIONS HERE
