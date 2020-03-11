from django import forms
from django.forms.widgets import NumberInput

class SQRPModelConfigForm(forms.Form):
    five_essentials_survey = forms.IntegerField(
                label="Five Essentials Survey", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    data_quality_index_score = forms.IntegerField(
                label="Data Quality Index Score", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    grade_9_psat_cohort_growth = forms.IntegerField(
                label="Grade 9: PSAT Cohort Growth", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    grade_10_psat_annual_growth_ebrw = forms.IntegerField(
                label="Grade 10: PSAT Annual Growth EBRW", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    grade_10_psat_annual_growth_math = forms.IntegerField(
                label="Grade 10: PSAT Annual Growth Math", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    grade_11_sat_3yr_cohort_growth = forms.IntegerField(
                label="Grade 11: SAT 3-year Cohort Growth", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    grade_11_sat_growth_ebrw = forms.IntegerField(
                label="Grade 11: SAT Growth EBRW", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    grade_11_sat_growth_math = forms.IntegerField(
                label="Grade 11: SAT Growth Math", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    priority_group_sat_growth = forms.IntegerField(
                label="Priority Group SAT Growth", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    avg_daily_attendance_rate = forms.IntegerField(
                label="Average Daily Attendance Rate", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    freshmen_on_track_rate = forms.IntegerField(
                label="Freshmen On Track To Graduate", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    four_year_cohort_graduation_rate = forms.IntegerField(
                label="Four-Year Cohort Graduation Rate", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    one_year_dropout_rate = forms.IntegerField(
                label="One Year Dropout Rate", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    percent_students_college_ready = forms.IntegerField(
                label="Percent College Ready Students", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    percent_graduating_with_creds = forms.IntegerField(
                label="Percent Graduating with Creds", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    college_enrollment_rate = forms.IntegerField(
                label="College Enrollment Rate", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    college_persistence_rate = forms.IntegerField(
                label="College Persistence Rate", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    attainment_psat_grade_9_school = forms.IntegerField(
                label="Grade 9 PSAT Attainment", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    attainment_psat_grade_10 = forms.IntegerField(
                label="Grade 10 PSAT Attainment", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))
    attainment_sat_grade_11_school = forms.IntegerField(
                label="Grade 11 SAT Attainment", 
                widget=NumberInput(attrs={
                'class': 'range-field',
                'type': 'range',
                'value': 0,
                'step': 1,
                "min": 0,
                "max": 6
            }))