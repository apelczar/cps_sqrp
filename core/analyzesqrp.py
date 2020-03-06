# CAPP 30122: Final Project - CPS SQRP Playground
# Winter 2020
# Ali Pelczar, Lily Grier, and Launa Greer
# 
# Processes a school quality rating policy (SQRP) for the Chicago Public
# Schools (CPS) by assigning rating and attainment scores for each high school
# in the district and then generating a bias score for the SQRP as a whole.

import sqlite3
import bias_score
from models import school, sqrp
import pandas as pd
#import school
#import sqrp

def process_sqrp(user_input):
    print("processing user input")
    for k, v in user_input.items():
        print(k, ":", v)

def main():
    '''
    The point of entry for the program.
    '''
    print("test main")

def calculate_sqrp_scores(policy):
    '''
    Calculate the SQRP scores and the bias score of a policy.

    Inputs:
        SQRP object

    Returns:
        school_lst: a list of School objects
        bias_score: an integer, 0-100
    '''

    school_records, enrollment = get_records()
    school_lst = []
    enrollment["sqrp_points"] = 0
    enrollment["rating"] = "Inability to Rate"
    for record in school_records:
        s_obj = school.School(record, policy)
        school_lst.append(s_obj)
        if s_obj.sqrp_rating != "Inability to Rate":
            enrollment.loc[str(s_obj.id), "sqrp_points"] = s_obj.sqrp_points
            enrollment.loc[str(s_obj.id), "rating"] = s_obj.sqrp_rating
    bias_score = bias_score.calculate_bias_score(enrollment)
    return school_lst, bias_score


def get_records():
    '''
    Obtains school records from the database.
    
    Inputs:
        none

    Returns:
        a list of dictionaries, where each dictionary represents a school
    '''

    conn = sqlite3.connect("../db.sqlite3")
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

if __name__ == '__main__':
    main()
