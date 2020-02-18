import pandas as pd
import xlrd
import re

filename = "Accountability_SQRPratings_2018-2019_SchoolLevel.xls"

#column_names = {"Unnamed: 1": df["Unnamed: 1"][0]}

# ADD METRIC TYPE COLUMN
def load_header_ows(filename):
    df = pd.read_excel(filename, sheet_name=2)


def load_data(filename, sheet_name): 
    '''
    Loads spreadsheet from row 4 down.
    '''
    df = pd.read_excel(filename, sheet_name, header=[1, 2])
    df.columns = [": ".join(col).strip() for col in df.columns.values]
    return df

def clean_hs_data(hs_data):
    cols_to_keep = ["School ID: Unnamed: 0_level_1", 
                    "School Name: Unnamed: 1_level_1",
                    "SY 2018-2019 SQRP Rating: Unnamed: 4_level_1"]
    for col in hs_data.columns:
        if re.search(r'Part. Rate', col) or re.search(r': Score', col):
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
        #re.sub(r'\s+', " ", col)
        #if col not in clean_names:
        clean_names[col] = col_clean
    return clean_names

def refine_and_clean_hs(hs_data):
    '''
    Makes smaller data frame with specified columns 
    '''
    names_dict = clean_hs_data(hs_data)
    cols_to_keep = list(names_dict.keys())
    pared_df = hs_data[cols_to_keep]
    pared_df = pared_df.rename(columns=names_dict)
    return pared_df

def rename_cols(hs_data):
    '''
    Renames remaining columns
    '''
    general_names = {"SAT11 EBRW Annual Growth Percentile": "grade_11_sat_growth_ebrw",
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
    "College Persistence Rate": "college_persistence_rate"
    "My Voice, My School 5 Essentials Survey": "five_essentials_survey",
    "Data Quality Index Score": "data_quality_index_score"}

    # MAKE SCORE AND PART DICT FROM GENERAL NAMES DICT

    



def clean_combo_data(combo_data):
    return None

def load_combo_data(filename):

    df = pd.read_excel(filename, sheet_name=3, header=[1, 2])


def rename_dict(df):
    '''
    Create dictionary for renaming cols using regex
    '''


def gen_col_name_dict(df):
    col_names = {}
    for col in df.columns:
        col_names[col] = df[col][0]
    return col_names



