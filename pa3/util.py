'''
Utility Function for Record Linkage Assignment
'''

import functools

def get_jw_category(jw_score):
    '''
    Convert a Jaro-Winkler score into a categorical: low, medium. high
    using fixed thresholds.

    Inputs:
        jw_score (float): value between 0 and 1 (inclusive)

    Returns: string
    '''

    thresh1 = 0.8
    thresh2 = 1.0

    if jw_score < thresh1:
        return "low"
    elif jw_score < thresh2:
        return "medium"
    return "high"


def sort_prob_tuples(tuples):
    '''
    Sort a list of probability tuples using the ordering specified in
    the assignment.

    Input:
       tuples (list): list of tuples of the form:
         ((similarity tuple), match probability, unmatch probability)

    Return: sorted list of tuples
    '''
    return sorted(tuples,
                  key=functools.cmp_to_key(cmp_tuples))


def cmp_sim_tuples(t1, t2):
    '''
    Compare two similarity tuples

    Inputs:
      t1, t2: similarity tuples

    Returns: value < 0, if val1 < val2 in the usual tuple ordering
             value == 0, if they are the same,
             value > 0 if va1 > val2 in the usual tuple ordering
    '''
    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    return 0

def cmp_tuples(val1, val2):
    '''
    Compare two probability tuples of the form:
       ((similarity tuple), match probability, unmatch probability)
    using the ordering specified in the assignment.

    Inputs:
      val1, val2 (tuples as shown above): values to compare

    Returns: value < 0, if val1 < val2 in the ordering,
             value == 0, if they are the same,
             value > 0 if va1 > val2 in the ordering.
    '''

    t1, m1, u1 = val1
    t2, m2, u2 = val2
    if (m1 == 0.0 and u1 == 0.0) or (m2 == 0.0 and u2 == 0.0):
        # this case should not occur
        raise Exception
    elif u1 == 0 and u2 == 0:
        diff = m2 - m1
        if diff == 0:
            v = cmp_sim_tuples(t1, t2)
            assert v != 0
            return v
        return diff
    elif u1 == 0:
        return -1
    elif u2 == 0:
        return 1

    diff = m2/u2 - m1/u1
    if diff == 0:
        v = cmp_sim_tuples(t1, t2)
        assert v != 0
        return v
    return diff
