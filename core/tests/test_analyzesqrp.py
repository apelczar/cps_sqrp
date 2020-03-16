'''
test_analyzesqrp.py
-------------------
Runs a few test cases addressing some edge cases, as well as the
current SQRP.
'''

from core.models import sqrp
from core import analyzesqrp

REL_WEIGHTS_TEST1 = {
    "grade_11_sat_3yr_cohort_growth": 0,
    "priority_group_sat_growth": 0,
    "grade_11_sat_growth_ebrw": 0,
    "grade_11_sat_growth_math": 0,
    "grade_10_psat_annual_growth_ebrw": 0,
    "grade_10_psat_annual_growth_math": 0,
    "grade_9_psat_cohort_growth": 0,
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
    "attainment_sat_grade_11_school": 0
}

REL_WEIGHTS_TEST2 = {
    "grade_11_sat_3yr_cohort_growth": 1,
    "priority_group_sat_growth": 1,
    "grade_11_sat_growth_ebrw": 1,
    "grade_11_sat_growth_math": 1,
    "grade_10_psat_annual_growth_ebrw": 1,
    "grade_10_psat_annual_growth_math": 1,
    "grade_9_psat_cohort_growth": 1,
    "percent_students_college_ready": 1,
    "avg_daily_attendance_rate": 1,
    "freshmen_on_track_rate": 1,
    "four_year_cohort_graduation_rate": 1,
    "one_year_dropout_rate": 1,
    "percent_graduating_with_creds": 1,
    "college_enrollment_rate": 1,
    "college_persistence_rate": 1,
    "five_essentials_survey": 1,
    "data_quality_index_score": 1,
    "attainment_psat_grade_9_school": 1,
    "attainment_psat_grade_10": 1,
    "attainment_sat_grade_11_school": 1
}

REL_WEIGHTS_TEST3 = {
    "grade_11_sat_3yr_cohort_growth": 0,
    "priority_group_sat_growth": 1,
    "grade_11_sat_growth_ebrw": 0,
    "grade_11_sat_growth_math": 0,
    "grade_10_psat_annual_growth_ebrw": 0,
    "grade_10_psat_annual_growth_math": 0,
    "grade_9_psat_cohort_growth": 0,
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
    "attainment_sat_grade_11_school": 0
}

REL_WEIGHTS_TEST4 = {
    "grade_11_sat_3yr_cohort_growth": 0,
    "priority_group_sat_growth": 0,
    "grade_11_sat_growth_ebrw": 0,
    "grade_11_sat_growth_math": 0,
    "grade_10_psat_annual_growth_ebrw": 0,
    "grade_10_psat_annual_growth_math": 0,
    "grade_9_psat_cohort_growth": 0,
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
    "attainment_psat_grade_9_school": 1,
    "attainment_psat_grade_10": 1,
    "attainment_sat_grade_11_school": 1
}

TEST_CASES = [(REL_WEIGHTS_TEST1, "N/A"),
              (REL_WEIGHTS_TEST2, 56),
              (REL_WEIGHTS_TEST3, 12),
              (REL_WEIGHTS_TEST4, 73),
              ({}, 53)]

def run_tests(test_lst=TEST_CASES):
    test_num = 1
    for test, expected_bias in test_lst:
        test_policy = sqrp.SQRP(test)
        school_lst, bias = analyzesqrp.calculate_sqrp_scores(test_policy)
        correct_len = "PASSED" if len(school_lst) == 135 else "FAILED"
        correct_bias = "PASSED" if bias == expected_bias else "FAILED"
        rv = '''Test number: {} \n
                Correct length: {} \n
                Correct bias score: {} \n\n'''.format(test_num, correct_len,
                                                      correct_bias)
        test_num += 1
        print(rv)