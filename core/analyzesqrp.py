# CAPP 30122: Final Project - CPS SQRP Playground
# Winter 2020
# Ali Pelczar, Lily Grier, and Launa Greer
# 
# Processes a school quality rating policy (SQRP) for the Chicago Public
# Schools (CPS) by assigning rating and attainment scores for each high school
# in the district and then generating a bias score for the SQRP as a whole.

import os
import json
import sqlite3
import pandas as pd
from core.models import bias_score as bs
from core.models.sqrp import SQRP
from core.models.school import School

def calculate_sqrp_scores(user_input):
    '''
    Calculate the SQRP scores and the bias score of a policy.

    Inputs:
        user_input (dict<str, float>): a dictionary with indicator names as keys
            and relative weights as values

    Returns:
        school_lst: a list of School objects
        bias_score: an integer, 0-100
    '''
    policy = SQRP(user_input)
    school_records, enrollment = get_records()
    school_lst = []
    enrollment["sqrp_points"] = 0
    enrollment["rating"] = "Inability to Rate"
    for record in school_records:
        s_obj = School(record, policy)
        school_lst.append(s_obj)
        if s_obj.sqrp_rating != "Inability to Rate":
            enrollment.loc[str(s_obj.id), "sqrp_points"] = s_obj.sqrp_points
            enrollment.loc[str(s_obj.id), "rating"] = s_obj.sqrp_rating
    bias_score = bs.calculate_bias_score(enrollment)
    return school_lst, bias_score


def get_records():
    '''
    Obtains school records from the database.
    
    Inputs:
        none

    Returns:
        a list of dictionaries, where each dictionary represents a school
    '''
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = "{}\db.sqlite3".format(root)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM sqrp JOIN location ON
                      sqrp.school_id = location.school_id;''')
    rows = cursor.fetchall()
    schools = [dict(r) for r in rows]
    enrollment = pd.read_sql_query("SELECT * FROM enrollment",
                                   conn, index_col="school_id")
    conn.close()
    return schools, enrollment