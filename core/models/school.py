###############
#
# School class for output
#
###############

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

NON_ASSESSMENT_REASSIGNMENT = [
        (percent_students_college_ready, reassign_readiness_weight),
        (college_persistence_rate, reassign_persistence_weight),
        (college_enrollment_rate, reassign_enrollment_weight),
        (four_year_cohort_graduation_rate, reassign_graduation_weight),
        (freshman_on_track_rate, reassign_on_track_weight),
        (avg_daily_attendance_rate, reassign_to_growth),
        (one_year_dropout_rate, reassign_to_growth),
        (percent_graduating_with_creds, reassign_to_growth),
        (five_essentials_survey, reassign_to_growth),
        (data_quality_index_score, reassign_to_growth)]

ASSESSMENT_INDICATORS = [grade_11_sat_3yr_cohort_growth,
                         grade_11_sat_growth_ebrw,
                         grade_11_sat_growth_math,
                         grade_10_psat_annual_growth_ebrw,
                         grade_10_psat_annual_growth_math,
                         grade_9_psat_cohort_growth]

class School():
    """
    Represents one school for output
    """

    def __init__(self, name, school_id, latitude, longitude, rating):
        '''
        Create a School object

        Inputs:
            name: (str) the name of the school
            id: (str) the unique ID of the school
            latitude, longitude (floats)
            cps_rating: (str) the school's rating under current SQRP

        '''

        self.name = name
        self.id = school_id
        self.location = (latitude, longitude)
        self.cps_rating = rating
        self.sqrp_points = 0
        self.sqrp_rating = "Inability to Rate"
        self.weights = EMPTY_WEIGHTS_DICT

    def assign_rating(self, points):
        '''
        Assign a rating to school based on the given point value.

        Inputs:
            points: float

        Outputs:
            none
        '''

        if total_points > 0 and total_points < 2.0:
            self.sqrp_rating = "Level 3"
        elif total_points >= 2.0 and total_points < 3.0:
            self.sqrp_rating = "Level 2"
        elif total_points >= 3.0 and total_points < 3.5:
            self.sqrp_rating = "Level 2+"
        elif total_points >= 3.5 and total_points < 4.0:
            self.sqrp_rating = "Level 1"
        else:
            self.sqrp_rating = "Level 1+"


    def calculate_points(self, indicators, policy, base_weight):
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
            total_points += self.calculate_points(indicator, function, policy)

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

        #First, calculate base numerical weights
        #Second, calculate priority group weights
        #Third, reassign weights as needed
        #Fourth, use the weights to calculate scores

        self.calculate_growth_weights(policy)
        for measure in ASSESSMENT_INDICATORS:
            total_points += self.weights[str(measure)] * indicators[measure]

        #Check that all weight has been reassigned
        #If it hasn't inflate currently calculated points to reflect full weighting
        total_weight = sum(self.weights.values())
        if total_weight != 1 and total_weight != 0:
            inflation = 1 / total_weight
            total_points = total_points * inflation
            for weight in self.weights.values():
                weight *= inflation

        return total_points


    def calculate_points(self, indicator, reassignment_function, policy):
        ind_weight = self.weights[str(indicator)] + (
            policy.indicator * policy.base_weight)
        if ind_weight > 0 and not indicators[indicator]:
            self.reassignment_function(ind_weight, indicators, policy)
            return 0
        else:
            self.weights[str(indicator)] = ind_weight
            return ind_weight * indicators[indicator]


    def reassign_readiness_weight(self, weight, indicators, policy):
        usable_indicators = []
        for indicator, fun in NON_ASSESSMENT_REASSIGNMENT[1:]:
            if indicators[indicator] and policy.indicator > 0:
                usable_indicators.append(indicator)
        if len(usable_indicators) == 0:
            return None
        reassigned_wt = 1 / len(usable_indicators)
        for indicator in usable_indicators:
            self.weights[indicator] = self.weights[indicator] + reassigned_wt

    def reassign_persistence_weight(self, weight, indicators, policy):
        if indicators[enrollment] and policy.college_enrollment_rate > 0:
            self.weights["college_enrollment_rate"] = (
                self.weights["college_enrollment_rate"] + weight)
        else:
            self.reassign_enrollment_weight(weight, indicators, policy)

    def reassign_enrollment_weight(self, weight, indicators, policy):
        if indicators[graduation_rate] and (
            policy.four_year_cohort_graduation_rate > 0):
            self.weights["four_year_cohort_graduation_rate"] = (
                self.weights["four_year_cohort_graduation_rate"] + weight)
        else:
            self.reassign_graduation_weight(weight, indicators, policy)

    def reassign_graduation_weight(self, weight, indicators, policy):
        rel_weight_total = 0
        weight_reassignment = {"freshman_on_track_rate": 2,
                               "avg_daily_attendance_rate": 1,
                               "one_year_dropout_rate": 1}
        for indicator, rel_weight in weight_reassignment.items():
            if policy.indicator > 0:
                rel_weight_total += rel_weight
        if rel_weight_total == 0:
            return None
        reassign_weight = 1 / rel_weight_total
        if indicators[freshman_on_track_rate] and policy.freshman_on_track_rate > 0:
            self.weights["freshman_on_track_rate"] = (
                self.weights["freshman_on_track_rate"] + (2 * reassign_weight))
        else:
            self.reassign_on_track_weight(2 * reassign_weight, indicators, policy)
        if indicators[attendance] and policy.avg_daily_attendance_rate > 0:
            self.weights["avg_daily_attendance_rate"] = (
                self.weights["avg_daily_attendance_rate"] + reassign_weight)
        else:
            self.reassign_to_growth(reassign_weight, indicators, policy)
        if indicators[one_year_dropout_rate] and policy.one_year_dropout_rate > 0:
            self.weights["one_year_dropout_rate"] = (
                self.weights["one_year_dropout_rate"] + reassign_weight)
        else:
            self.reassign_to_growth(reassign_weight, indicators, policy)


    def reassign_to_growth(self, weight, indicators, policy):
        '''
        Reassign the weight for average daily attendance, 1-year dropout rate,
        percent of graduates earning early credentials, 5 essentials survey,
        and data quality index score, in the case that a school is missing
        data for that indicator.

        Inputs:
            weight: the numerical weight for the category to be
                    redistributed (the relative weight * base weight)

        Returns:
            the points for that indicator, based on reassignment

        '''
        weight_reassignment = {grade_11_sat_3yr_cohort_growth: 2,
                               grade_11_sat_growth_ebrw: 1,
                               grade_11_sat_growth_math: 1,
                               grade_10_psat_annual_growth_ebrw: 1,
                               grade_10_psat_annual_growth_math: 1,
                               grade_9_psat_cohort_growth: 2}
        rel_weight_total = 0
        for indicator, rel_weight in weight_reassignment.items():
            if policy.indicator > 0:
                rel_weight_total += rel_weight
        if rel_weight_total == 0:
            return None
        reassigned_weight = weight * (1 / rel_weight_total)
        for indicator in ASSESSMENT_INDICATORS
            if policy.indicator > 0:
                self.weights[indicator] = self.weights[indicator] + (
                    weight * reassigned_weight * weight_reassignment[indicator])

    def calculate_priority_group_weights(self, policy):
        pass

    def calculate_growth_weights(self, policy):
        grade_level_growth_count = 0
        for measure in ASSESSMENT_INDICATORS[1:]:
            if policy.measure > 0 and indicators[measure]:
                grade_level_growth_count += 1

        #If all grade-level growth measures are missing and/or not included,
        #give any weight for them to cohort growth. If cohort growth is
        #also missing or not included, reassignment fails.
        if grade_level_growth_count == 0 and (not (
            indicators[grade_11_sat_3yr_cohort_growth]) or
            policy.grade_11_sat_3yr_cohort_growth == 0):
            return None
        if grade_level_growth_count == 0 and (
            indicators[grade_11_sat_3yr_cohort_growth]:
            for measure in ASSESSMENT_INDICATORS[1:]:
                m_weight = policy.measure * policy.base_weight
                self.weights[str(measure)] = self.weights[str(measure)] + m_weight

        grade_level_wt = 1 / grade_level_growth_count



