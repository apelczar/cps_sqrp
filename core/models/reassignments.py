'''
reassignments.py
'''
from core.models.indicators import ASSESSMENT_INDICATORS

def reassign_readiness_weight(school, weight, indicators, policy):
    '''
    Reassigns weight from the college readiness indicator.

    Inputs:
        school: a school object
        weight: (float) the numerical weight for college readiness
        indicators: (dict)
        policy: an SQRP object

    Returns:
        none
    '''

    usable_indicators = []
    rel_weight_total = 0
    for indicator, _ in NON_ASSESSMENT_REASSIGNMENT[1:]:
        if indicators[indicator] and policy.relative_weights[indicator]:
            usable_indicators.append(indicator)
            rel_weight_total += policy.relative_weights[indicator]
    if not usable_indicators:
        return
    reassigned_wt = weight / rel_weight_total
    for indicator in usable_indicators:
        school.weights[indicator] = school.weights[indicator] + reassigned_wt


def reassign_persistence_weight(school, weight, indicators, policy):
    '''
    Reassigns weight from the college persistence indicator.

    Inputs:
        school: a school object
        weight: (float) the numerical weight for college persistence
        indicators: (dict)
        policy: an SQRP object

    Returns:
        none
    '''

    school.weights["college_enrollment_rate"] = (
            school.weights["college_enrollment_rate"] + weight)


def reassign_enrollment_weight(school, weight, indicators, policy):
    '''
    Reassigns weight from the college enrollment indicator.

    Inputs:
        school: a school object
        weight: (float) the numerical weight for college enrollment
        indicators: (dict)
        policy: an SQRP object

    Returns:
        none
    '''

    school.weights["four_year_cohort_graduation_rate"] = (
            school.weights["four_year_cohort_graduation_rate"] + weight)


def reassign_graduation_weight(school, weight, indicators, policy):
    '''
    Reassigns weight from the graduation rate indicator.

    Inputs:
        school: a school object
        weight: (float) the numerical weight for graduation rate
        indicators: (dict)
        policy: an SQRP object

    Returns:
        none
    '''

    school.weights["freshmen_on_track_rate"] = (
        school.weights["freshmen_on_track_rate"] + (weight / 2))
    school.weights["avg_daily_attendance_rate"] = (
        school.weights["avg_daily_attendance_rate"] + (weight / 4))
    school.weights["one_year_dropout_rate"] = (
        school.weights["one_year_dropout_rate"] + (weight / 4))


def reassign_on_track_weight(school, weight, indicators, policy):
    '''
    Reassigns weight from the freshman on track indicator.

    Inputs:
        school: a school object
        weight: (float) the numerical weight for freshman on track
        indicators: (dict)
        policy: an SQRP object

    Returns:
        none
    '''

    school.weights["avg_daily_attendance_rate"] = (
        school.weights["avg_daily_attendance_rate"] + (weight / 2))
    school.weights["one_year_dropout_rate"] = (
        school.weights["one_year_dropout_rate"] + weight / 2)


def reassign_to_growth(school, weight, indicators, policy):
    '''
    Reassign the weight for average daily attendance, 1-year dropout rate,
    percent of graduates earning early credentials, 5 essentials survey,
    and data quality index score, in the case that a school is missing
    data for that indicator.

    Inputs:
        school: a school object
        weight: the numerical weight for the category to be redistributed
        indicators: (dict) the record for the school
        policy: an SQRP object

    Returns:
        none

    '''

    weight_reassignment = {"grade_11_sat_3yr_cohort_growth": 2,
                           "grade_11_sat_growth_ebrw": 1,
                           "grade_11_sat_growth_math": 1,
                           "grade_10_psat_annual_growth_ebrw": 1,
                           "grade_10_psat_annual_growth_math": 1,
                           "grade_9_psat_cohort_growth": 2}
    rel_weight_total = 0
    for indicator, rel_weight in weight_reassignment.items():
        if policy.relative_weights[indicator]:
            rel_weight_total += rel_weight

    if not rel_weight_total:
        return

    reassigned_weight = weight / rel_weight_total
    for indicator in ASSESSMENT_INDICATORS:
        if policy.relative_weights[indicator]:
            school.weights[indicator] = school.weights[indicator] + (
                reassigned_weight * weight_reassignment[indicator])


NON_ASSESSMENT_REASSIGNMENT = [
        ("percent_students_college_ready", reassign_readiness_weight),
        ("college_persistence_rate", reassign_persistence_weight),
        ("college_enrollment_rate", reassign_enrollment_weight),
        ("four_year_cohort_graduation_rate", reassign_graduation_weight),
        ("freshmen_on_track_rate", reassign_on_track_weight),
        ("avg_daily_attendance_rate", reassign_to_growth),
        ("one_year_dropout_rate", reassign_to_growth),
        ("percent_graduating_with_creds", reassign_to_growth),
        ("five_essentials_survey", reassign_to_growth),
        ("data_quality_index_score", reassign_to_growth)]