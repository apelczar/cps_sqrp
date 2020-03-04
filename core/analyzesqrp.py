# CAPP 30122: Final Project - CPS SQRP Playground
# Winter 2020
# Ali Pelczar, Lily Grier, and Launa Greer
# 
# Processes a school quality rating policy (SQRP) for the Chicago Public
# Schools (CPS) by assigning rating and attainment scores for each high school
# in the district and then generating a bias score for the SQRP as a whole.

import json
import os
from inspect import getsourcefile
from os.path import abspath

THIS_FOLDER = abspath(getsourcefile(lambda:0))
my_file = os.path.join(THIS_FOLDER, '/tests/mock_output.json')

def process_sqrp(user_input):
    print("processing user input")
    for k, v in user_input.items():
        print(k, ":", v)
    with open("C:/Users/greer/Documents/final_project/apelczar-launagreer-lilygrier/core/tests/mock_output.json", "r") as test_file:
        return json.load(test_file)

def main():
    '''
    The point of entry for the program.
    '''
    print("test main")

if __name__ == '__main__':
    main()
