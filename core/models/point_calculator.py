'''
point_calculator.py
'''
from core.models.indicators import ATTAINMENT_INDICATORS, ASSESSMENT_INDICATORS, PRIORITY_GROUP_INDICATORS
from core.models.reassignments import NON_ASSESSMENT_REASSIGNMENT

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
        total_points += calculate_ind_points(school, indicators,
                                             indicator, function, policy)

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

    total_points += calculate_add_input_points(school, indicators, policy)

    #Check that all weight has been reassigned
    #If it hasn't inflate currently calculated points according to their
    #relative weight
    total_weight = round(sum(school.weights.values()), 2)
    if total_weight != 1 and total_weight != 0:
        used_rel_weight_total = 0
        for indicator, weight in school.weights.items():
            if weight and indicator != "priority_group_sat_growth":
                used_rel_weight_total += policy.relative_weights[indicator]
        inflation_base = (1 - total_weight) / used_rel_weight_total
        for indicator in school.weights:
            if (school.weights[indicator] and indicator != 
                "priority_group_sat_growth"):
                added_weight = inflation_base * policy.relative_weights[indicator]
                total_points += indicators[indicator] * added_weight
                school.weights[indicator] = (school.weights[indicator]
                                             + added_weight)

    #add 0.001 to handle errors due to floating point values
    return total_points + 0.001


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
    if policy.relative_weights[indicator] and indicators[indicator]:
        school.weights[indicator] = ind_weight
        return ind_weight * indicators[indicator]
    elif ind_weight:
        reassignment_function(school, ind_weight, indicators, policy)
        school.weights[indicator] = 0
    return 0


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

def calculate_add_input_points(school, indicators, policy):
    '''
    Calculates weight for additional inputs (attainment scores)

    Inputs:
        indicators: (dict)
        policy: an SQRP object

    Returns:
        the points for all additional inputs
    '''

    points = 0
    weight_to_reassign = 0
    rel_weight_total = 0
    for item in ATTAINMENT_INDICATORS:
        item_weight = policy.relative_weights[item] * policy.base_weight
        if not indicators[item]:
            weight_to_reassign += item_weight
        else:
            rel_weight_total += policy.relative_weights[item]
            school.weights[item] = item_weight

    if not rel_weight_total:
        return points

    reassigned_weight = weight_to_reassign / rel_weight_total

    for item in ATTAINMENT_INDICATORS:
        if indicators[item] and school.weights[item]:
            school.weights[item] = school.weights[item] + reassigned_weight
            points += indicators[item] * school.weights[item]
    return points
