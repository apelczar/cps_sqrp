'''
indicators.py
-------------
Measures used by CPS to evaluate school quality.
'''

ALL_INDICATORS = ["five_essentials_survey",
                  "data_quality_index_score",
                  "grade_9_psat_cohort_growth",
                  "grade_10_psat_annual_growth_ebrw",
                  "grade_10_psat_annual_growth_math",
                  "grade_11_sat_3yr_cohort_growth",
                  "grade_11_sat_growth_ebrw",
                  "grade_11_sat_growth_math",
                  "priority_group_sat_growth",
                  "avg_daily_attendance_rate",
                  "freshmen_on_track_rate",
                  "four_year_cohort_graduation_rate",
                  "one_year_dropout_rate",
                  "percent_graduating_with_creds",
                  "percent_students_college_ready",
                  "college_enrollment_rate",
                  "college_persistence_rate",
                  "attainment_psat_grade_9_school",
                  "attainment_psat_grade_10",
                  "attainment_sat_grade_11_school"]

ASSESSMENT_INDICATORS = ["grade_11_sat_3yr_cohort_growth",
                         "grade_11_sat_growth_ebrw",
                         "grade_11_sat_growth_math",
                         "grade_10_psat_annual_growth_ebrw",
                         "grade_10_psat_annual_growth_math",
                         "grade_9_psat_cohort_growth"]

ATTAINMENT_INDICATORS = ["attainment_psat_grade_9_school",
                        "attainment_psat_grade_10",
                        "attainment_sat_grade_11_school"]

PRIORITY_GROUP_INDICATORS = ["aa_sat_growth",
                             "dl_sat_growth",
                             "el_sat_growth",
                             "hispanic_sat_growth"]
