from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .forms import SQRPConfigForm

import sys
sys.path.append('..')
from core import analyzesqrp

LABEL_DICT = {
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
    "College Persistence Rate": "college_persistence_rate"
}

def home(request):
    if request.method == "POST":
        try:
            processed = process_user_input(request.POST)
            analyzesqrp.process_sqrp(processed)
        except Exception as e:
            print('Exception caught', e)

        form = SQRPConfigForm(LABEL_DICT, request.POST)
    else:
        form = SQRPConfigForm(LABEL_DICT)
    
    return render(request, 'home.html', context={'form': form })


def process_user_input(query_dict):
    processed = {}
    for k in query_dict:
        if k in LABEL_DICT:
            processed[LABEL_DICT[k]] = query_dict[k]
    return processed