import json
import requests
import sqlite3
import pandas as pd

progress_report_url = "https://data.cityofchicago.org/resource/dw27-rash.json"
school_profile_url = "https://data.cityofchicago.org/resource/kh4r-387c.json"

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

location_vars = ["school_id",
                 "school_latitude",
                 "school_longitude"]

location_cols = {"school_id": str, 
                 "school_latitude": float, 
                 "school_longitude": float}

attainment_vars = ["school_id",
                   "attainment_psat_grade_9_school",
                   "attainment_psat_grade_10",
                   "attainment_sat_grade_11_school"]

attainment_cols = {"attainment_psat_grade_9_school": float,
                   "attainment_psat_grade_10": float,
                   "attainment_sat_grade_11": float}

#url1 = "https://data.cityofchicago.org/resource/kh4r-387c.csv"
def set_up_db():
    put_df_in_database(get_enrollment_data(), 'enrollment')
    put_df_in_database(get_location_data(), 'location')
    put_df_in_database(get_attainment_data(), 'attainment')

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
def get_attainment_data():
    '''
    Adds attainment data (maybe add more later) from progress report data
    '''
    url = "https://data.cityofchicago.org/resource/dw27-rash.json"
    query = "?$query=SELECT school_id, attainment_psat_grade_9_school, \
    attainment_psat_grade_10, attainment_sat_grade_11_school \
    WHERE primary_category = 'HS'"
    print("query looks like: ", url + query)
    attainment = requests.get(url + query)
    cols = {"attainment_psat_grade_9_school": float,
            "attainment_psat_grade_10": float,
            "attainment_sat_grade_11": float}
    attainment_data = attainment.text
    #print("attainment_data", attainment_data)
    df = pd.read_json(attainment_data, dtype=cols)
    #print("df looks like: ", df)
    return df

def attainment_to_percentile(attainment_df):
    return None


def get_location_data():
    url = "https://data.cityofchicago.org/resource/dw27-rash.json" # school profile api
    location_query = "?$query=SELECT school_id, school_latitude, school_longitude WHERE primary_category = 'HS'"
    location = requests.get(url + location_query)
    cols = {"school_id": str, "school_latitude": float, "school_longitude": float}
    location_data = location.text
    #print("location.text looks like: ", location.text)

    return pd.read_json(location_data, dtype=cols)


def get_enrollment_data():
    '''
    Makes request to CPS School Progress Report API
    '''
    url = "https://data.cityofchicago.org/resource/kh4r-387c.json"
    enrollment = requests.get(url + gen_enrollment_query())
    data = enrollment.text
    cols = {"school_id": str, "student_count_total": int,
    "student_count_low_income": int, "student_count_special_ed": int,
    "student_count_english_learners": int}
    df = pd.read_json(data, dtype=cols)
    print("df cols look like: ", df.columns)
    print("df looks like: ", df)
    df["percent_low_income"] = (df["student_count_low_income"] / 
                                df["student_count_total"])
    df["percent_english_learners"] = (df["student_count_english_learners"] / 
                                      df["student_count_total"])
    df["percent_special_ed"] = (df["student_count_special_ed"] / 
                                df["student_count_total"])
    cols_to_keep = ["school_id", "percent_low_income", "percent_english_learners",
    "percent_special_ed"]
    #for col in ["student_count_total", "student_count_low_income", 
        #"student_count_special_ed", "student_count_english_learners"]:
        #df.drop(col, axis=1, inplace=True)
    df = df[cols_to_keep]
    #df.drop(["student_count_total", "student_count_low_income", 
        #"student_count_special_ed", "student_count_english_learners"], inplace=True)
    #print("df cols looks like: ", df.columns)
    #print("type of data: ", type(data))
    return df

    #return enrollment_df.to_sql("enrollment")
    #with open('../data/enrollment.csv', 'w') as writer:
        #writer.write(enrollment.text)
    #return enrollment.text

def gen_enrollment_query():
    '''
    Generates query to select high school enrollment details from School Profile API
    '''
    enrollment_vars = ["school_id", "student_count_total", "student_count_low_income",
                       "student_count_special_ed", "student_count_english_learners"]
    query = "?$query=SELECT " + ", ".join(enrollment_vars) + " WHERE is_high_school = TRUE"

    return query

#def gen_progress_data_query():
    '''
    Generates a query to select info from School Progress Reports API
    '''
