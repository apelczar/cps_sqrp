import json
import requests
import sqlite3
import pandas as pd

PROGRESS_REPORT_URL = "https://data.cityofchicago.org/resource/dw27-rash.json"
SCHOOL_PROFILE_URL = "https://data.cityofchicago.org/resource/kh4r-387c.json"


def get_data(url, col_names, cols_dict):
    '''
    Calls the API endpoint using url, generates a query with specified columns, 
    and returns a Pandas dataframe.
    '''
    attributes = ", ".join(col_names)
    query = "?$query=SELECT " + attributes + " WHERE primary_category = 'HS'"
    request = requests.get(url + query)
    return pd.read_json(request.text, dtype=cols_dict)

def get_progress_report_data():
    '''
    Calls School Progress Report API and retrieves data on attainment and 
    location. Returns a Pandas dataframe.
    '''
    progress_vars = ["school_id",
                   "attainment_psat_grade_9_school",
                   "attainment_psat_grade_10",
                   "attainment_sat_grade_11_school",
                   "school_latitude",
                   "school_longitude"]

    progress_cols = {"attainment_psat_grade_9_school": float,
                   "attainment_psat_grade_10": float,
                   "attainment_sat_grade_11": float,
                   "school_latitude": float,
                   "school_longitude": float}
    df = get_data(PROGRESS_REPORT_URL, progress_vars, progress_cols)
    bins = pd.IntervalIndex.from_tuples([(0, 10), (10, 40), (40, 70), 
        (70, 90), (90, 101)], closed="left")
    labs = [1, 2, 3, 4, 5]
    for var in progress_vars:
        df[var] = pd.cut(df[var], bins=bins, labels=[1, 2, 3, 4, 5])
        #df[var] = pd.cut(df[var], bins=[0, 10, 40, 70, 90, 101], right=False, 
            #include_lowest=True, labels=labs)
        #df[var] = df[var].categories = [1, 2, 3, 4, 5]
    return df


def get_profile_data():
    '''
    Calls School Profile API and retrieves data on enrollment. Returns a 
    Pandas dataframe.
    '''

    enrollment_vars = ["school_id", 
                   "student_count_total", 
                   "student_count_low_income",
                   "student_count_special_ed", 
                   "student_count_english_learners"]

    enrollment_cols = {"school_id": str,
                   "student_count_total": int,
                   "student_count_low_income": int, 
                   "student_count_special_ed": int,
                   "student_count_english_learners": int}
    df = get_data(SCHOOL_PROFILE_URL, enrollment_vars, enrollment_cols)
    df["percent_low_income"] = (df["student_count_low_income"] / 
                                df["student_count_total"])
    df["percent_english_learners"] = (df["student_count_english_learners"] / 
                                      df["student_count_total"])
    df["percent_special_ed"] = (df["student_count_special_ed"] / 
                                df["student_count_total"])
    cols_to_keep = ["school_id", "percent_low_income", 
                    "percent_english_learners", "percent_special_ed"]
    return df[cols_to_keep]
