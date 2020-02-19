import pandas as pd
import xlrd
import re

filename = "Accountability_SQRPratings_2018-2019_SchoolLevel.xls"

#column_names = {"Unnamed: 1": df["Unnamed: 1"][0]}

def load_and_clean_file(sheet_name):
    filename = "Accountability_SQRPratings_2018-2019_SchoolLevel.xls"
    hs_data = load_data(filename, sheet_name)
    pared_df = pare_df(hs_data)
    #rename_cols(pared_df)
    return rename_cols(pared_df)



def load_data(filename, sheet_name): 
    '''
    Loads spreadsheet from row 4 down.
    '''
    df = pd.read_excel(filename, sheet_name, header=[1, 2])
    df.columns = [": ".join(col).strip() for col in df.columns.values]
    return df

def initial_clean(hs_data):
    #hs_data = load_data(filename, sheet_name)
    #cols_to_keep = ["School ID: Unnamed: 0_level_1", 
                    #"School Name: Unnamed: 1_level_1",
                    #"SY 2018-2019 SQRP Rating: Unnamed: 4_level_1"]
    cols_to_keep = []
    for col in hs_data.columns:
        #if re.search(r': Score', col):
        if re.search(r': Points|School ID|School Name', col):
            #re.sub(r' :', "", col)
            cols_to_keep.append(col)
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
        #if col not in clean_names:
        clean_names[col] = col_clean
    return clean_names

def pare_df(hs_data):
    '''
    Specifies columns to keep and cleans their names
    '''
    names_dict = initial_clean(hs_data)
    cols_to_keep = list(names_dict.keys())
    pared_df = hs_data[cols_to_keep]
    pared_df = pared_df.rename(columns=names_dict)
    #print("pared_df cols are: ", pared_df.columns)
    return pared_df

def rename_cols(pared_df):
    '''
    Assigns new names to all columns
    Inputs:
        a pared data frame
    '''

    var_names = {"School ID": "school_id",
    "School Name": "school_name",
    "SAT11 EBRW Annual Growth Percentile": "grade_11_sat_growth_ebrw",
    "SAT11 MATH Annual Growth Percentile": "grade_11_sat_growth_math",
    "PSAT10 EBRW Annual Growth Percentile": "grade_10_psat_annual_growth_ebrw",
    "PSAT10 MATH Annual Growth Percentile": "grade_10_psat_annual_growth_math",
    "PSAT09 Cohort Growth Percentile": "grade_9_psat_cohort_growth",
    "Percent Meeting College Readiness Benchmarks": "percent_students_college_ready",
    "Average Daily Attendance Rate": "avg_daily_attendance_rate",
    "Freshmen On-Track Rate": "freshmen_on_track_rate",
    "4-Year Cohort Graduation Rate": "4_year_cohort_graduation_rate",
    "1-Year Dropout Rate": "one_year_dropout_rate",
    r"% Earning Early College and Career Credentials": "percent_graduating_with_creds",
    "College Enrollment Rate": "college_enrollment_rate",
    "College Persistence Rate": "college_persistence_rate",
    "My Voice, My School 5 Essentials Survey": "five_essentials_survey",
    "Data Quality Index Score": "data_quality_index_score",
    "SAT11 African-American Cohort Growth Percentile": "aa_sat_growth",
    "SAT11 Hispanic Cohort Growth Percentile": "hispanic_sat_growth",
    "SAT11 English Learner Cohort Growth Percentile": "el_sat_growth",
    "SAT11 Diverse Learner Cohort Growth Percentile": "dl_sat_growth"
    }
    


    #var_names.update(non_score_vars) # merge dicts
    pared_df = pared_df[list(var_names.keys())] # remove extraneous variables
    final_df = pared_df.rename(columns=var_names)
    #print("pared_df cols are: ", pared_df.columns)


    return final_df


    



def clean_combo_data(combo_data):
    return None

def load_combo_data(filename):

    df = pd.read_excel(filename, sheet_name=3, header=[1, 2])



def gen_col_name_dict(df):
    col_names = {}
    for col in df.columns:
        col_names[col] = df[col][0]
    return col_names



