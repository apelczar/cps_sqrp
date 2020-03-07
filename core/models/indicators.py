'''
indicators.py
'''

BASE_INDICATOR_DICT = {"grade_11_sat_3yr_cohort_growth": 0,
                       "priority_group_sat_growth" : 0,
                       "grade_11_sat_growth_ebrw": 0,
                       "grade_11_sat_growth_math": 0,
                       "grade_10_psat_annual_growth_ebrw": 0,
                       "grade_10_psat_annual_growth_math": 0,
                       "grade_9_psat_cohort_growth" : 0,
                       "percent_students_college_ready": 0,
                       "avg_daily_attendance_rate": 0,
                       "freshmen_on_track_rate": 0,
                       "four_year_cohort_graduation_rate": 0,
                       "one_year_dropout_rate": 0,
                       "percent_graduating_with_creds": 0,
                       "college_enrollment_rate": 0,
                       "college_persistence_rate": 0,
                       "five_essentials_survey": 0,
                       "data_quality_index_score": 0,
                       "attainment_psat_grade_9_school": 0,
                       "attainment_psat_grade_10": 0,
                       "attainment_psat_grade_11_school": 0}

ASSESSMENT_INDICATORS = ["grade_11_sat_3yr_cohort_growth",
                         "grade_11_sat_growth_ebrw",
                         "grade_11_sat_growth_math",
                         "grade_10_psat_annual_growth_ebrw",
                         "grade_10_psat_annual_growth_math",
                         "grade_9_psat_cohort_growth"]

PRIORITY_GROUP_INDICATORS = ["aa_sat_growth",
                             "dl_sat_growth",
                             "el_sat_growth",
                             "hispanic_sat_growth"]

ATTAINMENT_INDICATORS = ["attainment_psat_grade_9_school",
                        "attainment_psat_grade_10",
                        "attainment_psat_grade_11_school"]

INDICATOR_LABEL_DICT = {
    "Five Essentials Survey": "five_essentials_survey",
    "Data Quality Index Score": "data_quality_index_score",
    "Grade 9: PSAT Cohort Growth": "grade_9_psat_cohort_growth",
    "Grade 10: PSAT Annual Growth EBRW": "grade_10_psat_annual_growth_ebrw",
    "Grade 10: PSAT Annual Growth Math": "grade_10_psat_annual_growth_math",
    "Grade 11: SAT 3-year Cohort Growth": "grade_11_sat_3yr_cohort_growth",
    "Grade 11: SAT Growth EBRW": "grade_11_sat_growth_ebrw",
    "Grade 11: SAT Growth Math": "grade_11_sat_growth_math",
    "Priority Group SAT Growth": "priority_group_sat_growth",
    "Average Daily Attendance Rate": "avg_daily_attendance_rate",
    "Freshmen On Track To Graduate": "freshmen_on_track_rate",
    "Four-Year Cohort Graduation Rate": "four_year_cohort_graduation_rate",
    "One Year Dropout Rate": "one_year_dropout_rate",
    "Percent Graduating with Creds": "percent_graduating_with_creds",
    "Percent College Ready Students": "percent_students_college_ready",
    "College Enrollment Rate": "college_enrollment_rate",
    "College Persistence Rate": "college_persistence_rate",
    "Grade 9 PSAT Attainment": "attainment_psat_grade_9_school",
    "Grade 10 PSAT Attainment": "attainment_psat_grade_10",
    "Grade 11 PSAT Attainment": "attainment_psat_grade_11_school",
}