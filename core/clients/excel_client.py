'''
excel_client.py
-------
Parse Excel file data from the Chicago Data Portal.
'''

import pandas as pd
import re
import sqlite3

FILENAME = "../data/Accountability_SQRPratings_2018-2019_SchoolLevel.xls"

def make_final_df():
    '''
    Create the final dataframe from the High School and Combination
    Schools pages on the SQRP Excel spreadsheet.

    Inputs:
        None

    Returns:
        (pd.DataFrame): the cleaned data
    '''
    hs_data = load_and_clean_file(2)
    combo_school_data = load_and_clean_file(3)
    final_df = pd.concat([hs_data, combo_school_data], axis=0)

    return final_df


def load_and_clean_file(sheet_name):
    '''
    Load and clean data from an Excel spreadsheet.

    Inputs:
        sheet_name (int): the sheet number to be loaded/cleaned

    Returns:
        (pd.DataFrame): the cleaned data
    '''
    hs_data = load_data(sheet_name)
    pared_df = pare_df(hs_data, sheet_name)

    return rename_cols(pared_df, sheet_name)


def load_data(sheet_name): 
    '''
    Load data from an Excel spreadsheet from row 4 down.

    Inputs:
        sheet_name (int): the sheet number to be loaded/cleaned

    Returns:
        (pd.DataFrame): the loaded data
    '''
    df = pd.read_excel(FILENAME, sheet_name, header=[1, 2])
    df.columns = [": ".join(col).strip() for col in df.columns.values]
    if sheet_name == 3: # drop elementary school survey col in combo sheet
        df.drop(df.columns[74], axis=1, inplace=True)
    return df


def initial_clean(hs_data, sheet_name):
    '''
    Remove excess spaces from column names for easier processing.

    Inputs:
        hs_data (pd.DataFrame): the loaded data
        sheet_name: sheet number from original Excel spreadsheet. The number
            2 indicates high school data and 3 indicates combo school data.

    Returns:
        (pd.DataFrame): the cleaned data
    '''
    cols_to_keep = []
    for col in hs_data.columns:
        if re.search(r': Points|School ID|School Name|SY 2018-2019 SQRP Rating', col):
            cols_to_keep.append(col)
        if sheet_name == 2: # hs only sheet
            if re.search(r'SQRP Total Points Earned', col):
                cols_to_keep.append(col)
        if sheet_name == 3: # combo sheet
            if re.search(r'High School SQRP Points Earned', col):
                cols_to_keep.append(col)
    clean_names = {}
    for col in cols_to_keep:
        col_clean = re.sub(r" :", ":", col)
        col_clean = re.sub(r"  ", " ", col_clean)
        col_clean = re.sub(r": Unnamed: \w+|: Points|\n", "", col_clean)
        clean_names[col] = col_clean
    return clean_names


def pare_df(hs_data, sheet_name):
    '''
    Specifies columns to keep and cleans their names.

    Inputs:
        hs_data (pd.DataFrame): data loaded from the Excel file
        sheet_name: sheet number from original Excel spreadsheet. The number
            2 indicates high school data and 3 indicates combo school data.

    Returns:
        (pd.DataFrame): the pared data
    '''
    names_dict = initial_clean(hs_data, sheet_name)
    cols_to_keep = list(names_dict.keys())
    pared_df = hs_data[cols_to_keep]
    pared_df = pared_df.rename(columns=names_dict)

    return pared_df


def rename_cols(pared_df, sheet_name):
    '''
    Assigns new names to all columns.

    Inputs:
        pared_df (pd.DataFrame): a Pandas dataframe with trimmed column names
        sheet_name: sheet number from original Excel spreadsheet.
            2 indicates high school data and 3 indicates combo school data

    Returns:
        (pd.DataFrame): a DataFrame with corrected column names
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

    pared_df = pared_df[list(var_names.keys())] # remove extraneous variables
    final_df = pared_df.rename(columns=var_names)

    return final_df
