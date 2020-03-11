'''
analyzesqrp.py
--------------
Processes a school quality rating policy (SQRP) for the Chicago Public
Schools (CPS) by assigning rating and attainment scores for each high school
in the district and then generating a bias score for the policy as a whole.
'''

import sqlite3
import pandas as pd
from core.clients import dbclient
from core.models import school, sqrp, bias_score

def calculate_sqrp_scores(policy):
    '''
    Calculate the SQRP scores and the bias score of a policy.

    Inputs:
        (SQRP): a School Quality Rating Policy (SQRP)

    Returns:
        school_lst (list of Schools): the CPS schools
        bias_score (int): an integer within the inclusive range of 0-100
    '''
    school_records, enrollment = dbclient.get_records()
    school_lst = []
    enrollment["sqrp_points"] = 0
    for record in school_records:
        s_obj = school.School(record, policy)
        school_lst.append(s_obj)
        if s_obj.sqrp_rating != "Inability to Rate":
            enrollment.loc[str(s_obj.id), "sqrp_points"] = s_obj.sqrp_points
    score = bias_score.calculate_bias_score(enrollment)
    return school_lst, score
