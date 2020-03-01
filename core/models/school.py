###############
#
# School class for output
#
###############

import sqlite3
conn = sqlite3.connect("../../db.sqlite3")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('''SELECT * FROM sqrp JOIN location ON
                  sqrp.school_id = location.school_id;''')
rows = cursor.fetchall()
schools = [dict(r) for r in rows]

#output = []
#for s in schools:
#    school_obj = School(s, policy)
#    #update table of scores for bias rating
#    output.append(s)

#return output

EMPTY_WEIGHTS_DICT = {"grade_11_sat_3yr_cohort_growth": 0,
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
                      "data_quality_index_score": 0
}





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



def calculate_points(school, indicators, policy):
    '''
    Calculate a rating under the user's policy
    Inputs:
        indicators: the school's record from the SQRP points database
        policy: an SQRP object
        base_weight: the base weight for the given policy

    Returns:
        the points that the school earned under the policy
    '''

    total_points = 0

    for indicator, function in NON_ASSESSMENT_REASSIGNMENT:
        total_points += calculate_ind_points(school, indicators, indicator,
                                                  function, policy)

    #1. Percent of students college-ready
    #2. College persistence rate
    #3. College enrollment rate
    #4. Graduation rate
    #5. Freshman-on-track rate
    #6. Average daily attendance
    #7. Dropout rate
    #8. Graduation with early college/career credentials
    #9. 5 Essentials Survey
    #10. Data Quality Index
    
    #Assessment indicators
    #Calculate priority group weights and points
    if policy.priority_group_sat_growth > 0:
        total_points += calculate_priority_group_points(school, indicators,
                                                             policy)
    
    #Calculate and reassign weights as needed
    calculate_growth_weights(school, indicators, policy)
    
    #Use the weights to calculate scores
    for measure in ASSESSMENT_INDICATORS:
        if indicators[measure]:
            total_points += school.weights[measure] * indicators[measure]

    #Check that all weight has been reassigned
    #If it hasn't inflate currently calculated points to reflect full weighting
    total_weight = sum(school.weights.values())
    if total_weight != 1 and total_weight != 0:
        inflation = 1 / total_weight
        total_points = total_points * inflation
        for ind, weight in school.weights.items():
            school.weights[ind] = weight * inflation

    return total_points


def calculate_ind_points(school, indicators, indicator,
                         reassignment_function, policy):
    '''
    Calculates the weight for the given indicator and, if possible,
    calculates the score for that indicator. If not, reassigns the
    weight according to the rules for that indicator.

    Note that this function must be run for all indicators, even if they
    have a relative weight of 0, because other indicators may
    reassign weight to them.

    Inputs:
        indicator: (str) the name of the indicator
        reassignment_function: to reassign weight if needed
        policy: an SQRP object

    Returns:
        (float) the points for that indicator
    '''

    ind_weight = school.weights[indicator] + (
        policy.relative_weights[indicator] * policy.base_weight)
    print(indicator, ind_weight)
    if policy.relative_weights[indicator] and indicators[indicator]:
        school.weights[indicator] = ind_weight
        return ind_weight * indicators[indicator]
    elif ind_weight:
        reassignment_function(school, ind_weight, indicators, policy)
        school.weights[indicator] = 0
    return 0


def reassign_readiness_weight(school, weight, indicators, policy):
    '''
    Reassigns weight from the college readiness indicator.

    Inputs:
        weight: (float) the numerical weight for college readiness
        indicators: (dict)
        policy: an SQRP object

    Returns:
        none
    '''

    usable_indicators = []
    for indicator, fun in NON_ASSESSMENT_REASSIGNMENT[1:]:
        if indicators[indicator] and policy.relative_weights[indicator]:
            usable_indicators.append(indicator)
    if not usable_indicators:
        return
    reassigned_wt = 1 / len(usable_indicators)
    for indicator in usable_indicators:
        school.weights[indicator] = school.weights[indicator] + reassigned_wt

def reassign_persistence_weight(school, weight, indicators, policy):
    '''
    Reassigns weight from the college persistence indicator.

    Inputs:
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
        weight: (float) the numerical weight for graduation rate
        indicators: (dict)
        policy: an SQRP object

    Returns:
        none
    '''

    rel_weight_total = 0
    weight_reassignment = {"freshmen_on_track_rate": 2,
                           "avg_daily_attendance_rate": 1,
                           "one_year_dropout_rate": 1}
    for indicator, rel_weight in weight_reassignment.items():
        if indicators[indicator] and policy.relative_weights[indicator]:
            rel_weight_total += rel_weight

    if not rel_weight_total:
        return
    reassigned_weight = 1 / rel_weight_total

    #Note that in this situation, the weight is only distributed
    #if available. So, we must check here that we can reassign.
    for indicator, rel_weight in weight_reassignment.items():
        if indicators[indicator] and policy.relative_weights[indicator]:
            school.weights[indicator] = (school.weights[indicator]
                + (weight * rel_weight * reassigned_weight))


def reassign_on_track_weight(school, weight, indicators, policy):
    '''
    Reassigns weight from the freshman on track indicator.

    Inputs:
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
        weight: the numerical weight for the category to be
                redistributed
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

    reassigned_weight = weight * (1 / rel_weight_total)
    for indicator in ASSESSMENT_INDICATORS:
        if policy.relative_weights[indicator]:
            school.weights[indicator] = school.weights[indicator] + (
                weight * reassigned_weight * weight_reassignment[indicator])


def calculate_priority_group_points(school, indicators, policy):
    '''
    Calculates the points for the 11th grade SAT priority groups.
    Also reassigns weight as needed.

    Inputs:
        indicators: (dict)
        policy: an SQRP object

    Returns:
        (float) the points for the priority group category

    '''
    priority_num_weight = (policy.relative_weights["priority_group_sat_growth"] * 
                           policy.base_weight) / 4
    priority_points = 0
    priority_group_weight = 0
    for group in PRIORITY_GROUP_INDICATORS:
        if indicators[group]:
            priority_points += indicators[group] * priority_num_weight
            priority_group_weight += priority_num_weight
        else:
            school.weights["grade_11_sat_3yr_cohort_growth"] = (
                school.weights["grade_11_sat_3yr_cohort_growth"] +
                priority_num_weight)
    school.weights["priority_group_sat_growth"] = priority_group_weight
    return priority_points


def calculate_growth_weights(school, indicators, policy):
    '''
    Calculates the weights for all SAT growth measures other than
    priority groups

    Inputs:
        indicators: (dict)
        policy: an SQRP object

    Returns:
        none
    '''

    #Get base numerical weights
    for indicator in ASSESSMENT_INDICATORS:
        school.weights[indicator] = school.weights[indicator] + (
        policy.relative_weights[indicator] * policy.base_weight)

    grade_level_growth_count = 0
    grade_level_growth_weight = 0
    weight_to_reassign = 0
    for measure in ASSESSMENT_INDICATORS[1:]:
        if policy.relative_weights[measure] and indicators[measure]:
            grade_level_growth_count += 1
        else:
            weight_to_reassign += school.weights[measure]
            school.weights[measure] = 0

    #If all grade-level growth measures are missing and/or not included,
    #give any weight for them to cohort growth. If cohort growth is
    #also missing or not included, reassignment fails.
    if not grade_level_growth_count:
        if (indicators["grade_11_sat_3yr_cohort_growth"] and
        policy.grade_11_sat_3yr_cohort_growth):
            school.weights["grade_11_sat_3yr_cohort_growth"] = (
            school.weights["grade_11_sat_3yr_cohort_growth"] +
            weight_to_reassign)
        else:
            school.weights["grade_11_sat_3yr_cohort_growth"] = 0
        return


    #If there is weight to reassign among one-year growth indicators:
    reassigned_weight = weight_to_reassign * (1 / grade_level_growth_count)
    #and also reassign 3-yr growth if needed
    if (policy.grade_11_sat_3yr_cohort_growth and not 
        indicators["grade_11_sat_3yr_cohort_growth"]):
        reassigned_weight += school.weights["grade_11_sat_3yr_cohort_growth"] * (
            1 / grade_level_growth_count)
        school.weights["grade_11_sat_3yr_cohort_growth"] = 0
    for measure in ASSESSMENT_INDICATORS[1:]:
        if policy.relative_weights[measure] and indicators[measure]:
            school.weights[measure] = school.weights[measure] + reassigned_weight


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



class School():
    """
    Represents one school for output
    """

    def __init__(self, record, policy):
        '''
        Create a School object

        Inputs:
            record: (dict) one record from the sqrp table
            policy: an SQRP object

        '''

        self.name = record["school_name"]
        self.id = record["school_id"]
        self.location = (record["school_latitude"], record["school_longitude"])
        self.cps_rating = record["current_sqrp_rating"]
        self.weights = EMPTY_WEIGHTS_DICT
        self.sqrp_points = round(calculate_points(self, record, policy), 1)
        self.sqrp_rating = self.assign_rating(self.sqrp_points)


    def assign_rating(self, points):
        '''
        Assign a rating to school based on the given point value.

        Inputs:
            points: float

        Outputs:
            (str) the school's rating
        '''

        if points == 0 or self.cps_rating == "Inability to Rate":
            return "Inability to Rate"
        elif points > 0 and points < 2.0:
            return "Level 3"
        elif points >= 2.0 and points < 3.0:
            return "Level 2"
        elif points >= 3.0 and points < 3.5:
            return "Level 2+"
        elif points >= 3.5 and points < 4.0:
            return "Level 1"
        else:
            return "Level 1+"