import json
import requests
import sqlite3
import pandas as pd

#url1 = "https://data.cityofchicago.org/resource/kh4r-387c.csv"
def set_up_db():
    put_df_in_database(get_enrollment_data(), 'enrollment')
    put_df_in_database(get_location_data(), 'location')
    put_df_in_database(get_additional_inputs(), 'additional_inputs')

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
def get_additional_inputs():
    '''
    Adds attainment data (maybe add more later)
    '''
    url = "https://data.cityofchicago.org/resource/dw27-rash.json"
    query = '''?$query=SELECT attainment_psat_grade_9_school, attainment_psat_grade_10, 
            attainment_sat_grade_11'''
    additional_inputs = requests.get(url + query)
    cols = {"attainment_psat_grade_9_school": float,
            "attainment_psat_grade_10": float,
            "attainment_sat_grade_11": float}
    return pd.read_json(additional_inputs, dtype=cols)



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
    df["percent_low_income"] = (df["student_count_low_income"] / 
                                df["student_count_total"])
    df["percent_english_learners"] = (df["student_count_english_learners"] / 
                                      df["student_count_total"])
    df["percent_special_ed"] = (df["student_count_special_ed"] / 
                                df["student_count_total"])
    df.drop("student_count_total", "student_count_low_income", 
        "student_count_special_ed", "student_count_english_learners")
    #print("data looks like: ", data)
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
