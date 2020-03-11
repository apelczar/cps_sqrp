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

def get_social_media_data():
  '''
  Calls School Profile API and retrieves information on school social
  media information. Returns a Pandas dataframe.
  '''
  social_media_vars = ["school_id",
                       "facebook",
                       "twitter",
                       "youtube",
                       "pinterest"]

  social_media_cols = {"facebook": str,
                       "twitter": str,
                       "youtube": str,
                       "pinterest": str}
  return get_data(SCHOOL_PROFILE_URL, social_media_vars, social_media_cols)

def get_progress_report_data():
    '''
    Calls School Progress Report API and retrieves data on attainment and 
    location. Returns a Pandas dataframe.
    '''
    progress_vars = ["school_id",
                    "school_latitude",
                    "school_longitude",
                    "address",
                    "city",
                    "state",
                    "zip",
                    "phone",
                    "website"]
    
    attainment_vars = ["attainment_psat_grade_9_school",
                       "attainment_psat_grade_10",
                       "attainment_sat_grade_11_school"]

    progress_cols = {"attainment_psat_grade_9_school": float,
                   "attainment_psat_grade_10": float,
                   "attainment_sat_grade_11": float,
                   "school_latitude": float,
                   "school_longitude": float,
                   "address": str,
                   "city": str,
                   "state": str,
                   "zip": str,
                   "phone": str,
                   "website": str}

    df = get_data(PROGRESS_REPORT_URL, progress_vars + attainment_vars, 
                  progress_cols)
    bins = pd.IntervalIndex.from_tuples([(0, 10), (10, 40), (40, 70), 
        (70, 90), (90, 101)], closed="left")
    labs = [1, 2, 3, 4, 5]
    for var in attainment_vars:
        x = pd.cut(df[var].to_list(), bins=bins)
        x.categories = [1, 2, 3, 4, 5]
        df[var] = x

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
                       "student_count_english_learners",
                       "facebook",
                       "twitter",
                       "youtube",
                       "pinterest"]

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
    cols_to_keep = ["school_id", 
                    "percent_low_income", 
                    "percent_english_learners", 
                    "percent_special_ed"]

    return df[cols_to_keep]
