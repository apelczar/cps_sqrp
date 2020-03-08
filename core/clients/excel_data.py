import pandas as pd
import xlrd
import re
import sqlite3

filename = "Accountability_SQRPratings_2018-2019_SchoolLevel.xls"


def import_to_database(): # NEED TO MAKE DATABASE A PARAM IF I WANT TO IMPORT FUNCTION FROM APICLIENT
    df = make_final_df()
    #print("final_df looks like: ", df)
    con = sqlite3.connect("../db.sqlite3") # make sure this accesses database
    u = con.cursor()
    df.to_sql('sqrp', con=con, index=False, if_exists='append')
    return None


def make_final_df():
    hs_data = load_and_clean_file(2)
    combo_school_data = load_and_clean_file(3)
    final_df = pd.concat([hs_data, combo_school_data], axis=0)

    return final_df

def load_and_clean_file(sheet_name):
    filename = "Accountability_SQRPratings_2018-2019_SchoolLevel.xls"
    hs_data = load_data(filename, sheet_name)
    pared_df = pare_df(hs_data, sheet_name)

    return rename_cols(pared_df, sheet_name)


def load_data(filename, sheet_name): 
    '''
    Loads spreadsheet from row 4 down.
    '''
    df = pd.read_excel(filename, sheet_name, header=[1, 2])
    df.columns = [": ".join(col).strip() for col in df.columns.values]
    if sheet_name == 3: # drop elementary school survey col in combo sheet to avoid future confusion
        df.drop(df.columns[74], axis=1, inplace=True)
    return df

def initial_clean(hs_data, sheet_name): # JUST ADDED SHEET_NAME VAR
    #hs_data = load_data(filename, sheet_name)
    cols_to_keep = []
    for col in hs_data.columns:
        #if re.search(r': Score', col):
        if re.search(r': Points|School ID|School Name|SY 2018-2019 SQRP Rating', col):
            #re.sub(r' :', "", col)
            cols_to_keep.append(col)
        if sheet_name == 2:
            if re.search(r'SQRP Total Points Earned', col):
                cols_to_keep.append(col)
        if sheet_name == 3: # combo sheet
            if re.search(r'High School SQRP Points Earned', col):
                cols_to_keep.append(col)
        #elif sheet_name
    clean_names = {}
    #print("cols to keep: ", cols_to_keep)
    for col in cols_to_keep:
        # FIGURE OUT HOW TO DO THIS WITH SINGLE REGEX:
        # TAKE OUT DOUBLE SPACES AND SPACES BEFORE COLONS
        # TAKE OUT '\n'
        # REMOVE UNNAMED AND EVERYTHING AFTER
        col_clean = col.replace(" :", ":") # get rid of whitespace before colon
        col_clean = col_clean.replace("  ", " ") # get rid of second whitespace
        col_clean = col_clean.replace("\n", "")
        col_clean = re.sub(r": Unnamed: \w+", "", col_clean)
        col_clean = re.sub(r": Points", "", col_clean)
        #re.sub(r'\s+', " ", col)
        clean_names[col] = col_clean
    #print("clean_names columns", clean_names.keys())
    return clean_names

def pare_df(hs_data, sheet_name):
    '''
    Specifies columns to keep and cleans their names
    '''
    names_dict = initial_clean(hs_data, sheet_name)
    cols_to_keep = list(names_dict.keys())
    #print("cols_to_keep looks like: ", cols_to_keep)
    pared_df = hs_data[cols_to_keep]
    pared_df = pared_df.rename(columns=names_dict)

    return pared_df


def rename_cols(pared_df, sheet_name): # ADDED SHEET NAME AS INPUT
    '''
    Assigns new names to all columns
    Inputs:
        a pared data frame
    '''

    var_names = {"School ID": "school_id",
    "School Name": "school_name",
    "SAT11 Cohort Growth Percentile": "grade_11_sat_3yr_cohort_growth",
    "SAT11 EBRW Annual Growth Percentile": "grade_11_sat_growth_ebrw",
    "SAT11 MATH Annual Growth Percentile": "grade_11_sat_growth_math",
    "PSAT10 EBRW Annual Growth Percentile": "grade_10_psat_annual_growth_ebrw",
    "PSAT10 MATH Annual Growth Percentile": "grade_10_psat_annual_growth_math",
    "PSAT09 Cohort Growth Percentile": "grade_9_psat_cohort_growth",
    "Percent Meeting College Readiness Benchmarks": "percent_students_college_ready",
    "Average Daily Attendance Rate": "avg_daily_attendance_rate",
    "Freshmen On-Track Rate": "freshmen_on_track_rate",
    "4-Year Cohort Graduation Rate": "four_year_cohort_graduation_rate",
    "1-Year Dropout Rate": "one_year_dropout_rate",
    r"% Earning Early College and Career Credentials": "percent_graduating_with_creds",
    "College Enrollment Rate": "college_enrollment_rate",
    "College Persistence Rate": "college_persistence_rate",
    "My Voice, My School 5 Essentials Survey": "five_essentials_survey",
    "Data Quality Index Score": "data_quality_index_score",
    "SAT11 African-American Cohort Growth Percentile": "aa_sat_growth",
    "SAT11 Hispanic Cohort Growth Percentile": "hispanic_sat_growth",
    "SAT11 English Learner Cohort Growth Percentile": "el_sat_growth",
    "SAT11 Diverse Learner Cohort Growth Percentile": "dl_sat_growth",
    "SY 2018-2019 SQRP Rating": "current_sqrp_rating"
    }
    print("pared_df cols before renaming: ", pared_df.columns)

    #if sheet_name == 2:
        #var_names["SQRP Total Points Earned"] = "current_sqrp_points"
        #var_names['SY 2018-2019 SQRP Rating: Unnamed: 8_level_1'] = "current_sqrp_points"
    
    #if sheet_name == 3:
        #var_names['High School SQRP Points Earned: Unnamed: 5_level_1'] = "current_sqrp_points"
    #'High School SQRP Points Earned: Unnamed: 5_level_1'
    print("var_names looks like: ", var_names)

    pared_df = pared_df[list(var_names.keys())] # remove extraneous variables
    final_df = pared_df.rename(columns=var_names)

    return final_df



