import json
import csv
import requests
import sqlite3
import pandas as pd

#url1 = "https://data.cityofchicago.org/resource/kh4r-387c.csv"
def set_up_db():
    put_df_in_database(get_enrollment_data(), 'enrollment')
    put_df_in_database(get_location_data(), 'location')

def put_df_in_database(data_gen_func, table_name):
    df = data_gen_func
    con = sqlite3.connect("../../db.sqlite3")
    u = con.cursor()
    df.to_sql(table_name, con=con, index=False, if_exists='append')

#def put_loc_in_database():
    #df = get_location_data()
    #con = sqlite3.connect("../../db.sqlite3")
    #u = con.cursor()
    #df.to_sql('location', con=con, index=False, if_exists='append')
#def generate_enrollment_csv():
    #with open('enrollment.csv', 'w') as writer:
        #writer.write(enrollment.text)
def get_location_data():
    url = "https://data.cityofchicago.org/resource/dw27-rash.json"
    location_query = "?$query=SELECT school_id, school_latitude, school_longitude WHERE is_high_school = TRUE"
    location = requests.get(url + location_query)
    cols = {school_id: str, school_latitude: float, school_longitude = float}
    location_data = location.text

    return pd.read_json(location_data, dtype=cols)


def get_enrollment_data():
    url = "https://data.cityofchicago.org/resource/kh4r-387c.json"
    enrollment = requests.get(url + gen_enrollment_query())
    data = enrollment.text
    cols = {"school_id": str, "student_count_total": int,
    "student_count_low_income": int, "student_count_special_ed": int,
    "student_count_english_learners": int, "student_count_black": int, "student_count_hispanic": int,
    "student_count_white": int, "student_count_asian": int, "student_count_native_american": int,
    "student_count_other_ethnicity": int, "student_count_asian_pacific": int, "student_count_multi": int,
    "student_count_hawaiian_pacific": int, "student_count_ethnicity_not": int, "bilingual_services": bool,
    "refugee_services": bool, "title_1_eligible": bool}
    #print("data looks like: ", data)
    #print("type of data: ", type(data))
    return pd.read_json(data, dtype=cols)

    #return enrollment_df.to_sql("enrollment")
    #with open('../data/enrollment.csv', 'w') as writer:
        #writer.write(enrollment.text)
    #return enrollment.text

def gen_enrollment_query():
    '''
    Generates query to select high school enrollment details from School Profile API
    '''
    enrollment_vars = ["school_id", "student_count_total", "student_count_low_income",
                       "student_count_special_ed", "student_count_english_learners",
                       "student_count_black", "student_count_hispanic", 
                       "student_count_white", "student_count_asian",
                       "student_count_native_american", 
                       "student_count_other_ethnicity", "student_count_asian_pacific",
                       "student_count_multi", "student_count_hawaiian_pacific",
                       "student_count_ethnicity_not", "bilingual_services",
                       "refugee_services", "title_1_eligible"]
    query = "?$query=SELECT " + ", ".join(enrollment_vars) + " WHERE is_high_school = TRUE"

    return query

#def gen_progress_data_query():
    '''
    Generates a query to select info from School Progress Reports API
    '''
