'''
CAPP 30122: Test code for Speaker Attribution (Markov Model) assignment

Lamont Samuels
January 2019
'''
# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg= missing-docstring, line-too-long, too-many-locals
# pylint: disable-msg= too-many-locals

from itertools import permutations
import os
import pytest

from hash_table import HashTable

# Get the name of the directory that holds the grading code.
BASE_DIR = os.path.dirname(__file__)

KEY1 = "key"

################## Simple Hash Table Tests##################
def helper_update(table, test_dict):
    '''
    Purpose: Adds a test dictionary key, values to a HashTable object
    '''
    for key, value in test_dict.items():
        table.update(key, value)


def helper_lookup(table, expected_results):
    '''
    Purpose: helper function for testing lookup

    Inputs:
        table: (HashTable) the hash table used to perform the lookup
        key: (string) a string to lookup in the hash table
    '''
    test_keys = list(expected_results.keys())

    # 1st: Call lookup on the test_keys
    actual_results = []
    for key in test_keys:
        actual_results.append(table.lookup(key))


    # 2nd: Check to the actual results to see if they match the expected values
    failed = False
    expected_values = list(expected_results.values())
    for idx, actual_result in enumerate(actual_results):
        expected_result = expected_values[idx]
        if expected_result is None:
            if actual_result is not None:
                failed = True
                break
        elif actual_result != expected_result:
            failed = True
            break

    if failed:
        actual_results = dict(zip(test_keys, actual_results))
        s = ("Expected (key, value) pairs ({:}) \n\n\n and actual "
             "(key, value) pairs ({:}) do not match in hash table.")
        pytest.fail(s.format(expected_results, actual_results))

def test_simple_1():
    '''
    Purpose: Test a lookup on an empty table
    '''
    table = HashTable(1, None)
    helper_lookup(table, {KEY1:None})

def test_simple_2():
    '''
    Purpose: Test a update/lookup on a single item
    '''
    table = HashTable(1, None)
    table.update("key", 1)
    helper_lookup(table, {KEY1:1})

def test_simple_3():
    '''
    Purpose: Test a update/lookup on a small set of items
    '''
    keys = [''.join(tup) for tup in list(permutations("abc"))]
    test_dict = dict(zip(keys, range(len(keys))))
    table = HashTable(50, None)
    helper_update(table, test_dict)
    helper_lookup(table, test_dict)

def test_simple_4():
    '''
    Purpose: Test an update/lookup on a small set of items with
    some of the keys not being inside of the hash table
    '''
    keys = [''.join(tup) for tup in list(permutations("abc"))]
    test_dict = dict(zip(keys, range(len(keys))))
    table = HashTable(50, None)
    helper_update(table, test_dict)

    # Add to the test dictionary of a set of keys that will NOT be in
    # the dictionary they should all return the default value, which
    # in this case is "None"
    not_table_keys = [''.join(tup) for tup in list(permutations("test"))]
    not_table_values = [None] * len(not_table_keys)
    test_dict.update(dict(zip(not_table_keys, not_table_values)))

    helper_lookup(table, test_dict)

def test_simple_5():
    '''
    Purpose: Test a update/lookup on a larger set of items
    '''
    keys = [''.join(tup) for tup in list(permutations("abcefgh"))]
    test_dict = dict(zip(keys, range(len(keys))))
    table = HashTable(12000, None)
    helper_update(table, test_dict)
    helper_lookup(table, test_dict)

def test_simple_6():
    '''
    Purpose: Test a update/lookup on a larger set of items
        1st: Adding an initial set of key/value pairs
        2nd: Updating the values for the original key value pairs
    '''
    keys = [''.join(tup) for tup in list(permutations("abcefgh"))]
    test_dict1 = dict(zip(keys, range(len(keys))))
    test_dict2 = dict(zip(keys, [i + 100 for i in range(len(keys))]))
    table = HashTable(12000, None)
    helper_update(table, test_dict1)
    helper_update(table, test_dict2)
    helper_lookup(table, test_dict2)

################## Rehash Hash Table Tests ##################
def test_rehash_1():
    '''
    Purpose: Testing rehashing on a small set of items
    '''
    table = HashTable(1, None)
    keys = [''.join(tup) for tup in list(permutations("abcd"))]
    test_dict1 = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict1)
    helper_lookup(table, test_dict1)

def test_rehash_2():
    '''
    Purpose: Testing rehashing on a larger set of items
    '''
    table = HashTable(1, None)
    keys = [''.join(tup) for tup in list(permutations("abcefgh"))]
    test_dict1 = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict1)
    helper_lookup(table, test_dict1)

def test_rehash_3():
    '''
    Purpose: Test rehashing on a small set that wraps around
    '''
    keys = [chr(i) for i in range(ord('f'), ord('z'))]
    test_dict1 = dict(zip(keys, range(len(keys))))
    table = HashTable(15, None)
    helper_update(table, test_dict1)
    helper_lookup(table, test_dict1)
