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
                      "college_persistent_rate": 0,
                      "five_essentials_survey": 0,
                      "data_quality_index_score": 0
}

class School():
    """
    Represents one school for output
    """

    def __init__(self, name, school_id, latitude, longitude, rating):
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

        #1. Percent of students college-ready
        readiness_weight = policy.percent_students_college_ready * base_weight
        if readiness_weight > 0 and not indicators[readiness]:
            self.reassign_readiness_weight(readiness_weight)
        else:
            total_points += readiness_weight * indicators[readiness]
            self.weights["percent_students_college_ready"] = readiness_weight

        #2. College persistence rate
        persistence_weight = self.weights["college_persistent_rate"] + (
            policy.college_persistent_rate * base_weight)
        if persistence_weight > 0 and not indicators[persistence]:
            self.reassign_persistence_weight(persistence_weight)
        else:
            total_points += persistence_weight * indicators[persistence]
            self.weights["college_persistent_rate"] = persistence_weight

        #3. College enrollment rate
        enrollment_weight = self.weights["college_enrollment_rate"] + (
            policy.college_enrollment_rate * base_weight)
        if enrollment_weight > 0 and not indicators[enrollment]:
            self.reassign_enrollment_weight(enrollment_weight)
        else:
            total_points += enrollment_weight * indicators[enrollment]
            self.weights["college_enrollment_rate"] = enrollment_weight

        #4. Graduation rate
        graduation_weight = self.weights["four_year_cohort_graduation_rate"] + (
            policy.four_year_cohort_graduation_rate * base_weight)
        if graduation_weight > 0 and not indicators[graduation_rate]:
            self.reassign_graduation_weight(graduation_weight)
        else:
            total_points += graduation_weight * indicators[graduation_rate]
            self.weights["four_year_cohort_graduation_rate"] = graduation_weight

        #5. Freshman-on-track rate
        on_track_weight = self.weights["freshman_on_track_rate"] + (
            policy.freshman_on_track_rate * base_weight)
        if on_track_weight > 0 and not indicators[freshman_on_track_rate]:
            self.reassign_on_track_weight(on_track_weight)
        else:
            total_points += on_track_weight * indicators[freshman_on_track_rate]
            self.weights["freshman_on_track_rate"] = on_track_weight

        #6. Average daily attendance
        attendance_weight = self.weights["avg_daily_attendance_rate"] + (
            policy.avg_daily_attendance_rate * base_weight)
        if attendance_weight > 0 and not indicators[attendance]:
            self.reassign_to_growth(attendance_weight, indicators, policy)
        else:
            total_points += attendance_weight * indicators[attendance]
            self.weights["avg_daily_attendance_rate"] = attendance_weight

        #7. Dropout rate
        dropout_weight = self.weights["one_year_dropout_rate"] + (
            policy.one_year_dropout_rate * base_weight)
        if dropout_weight > 0 and not indicators[one_year_dropout_rate]:
            self.reassign_to_growth(dropout_weight, indicators, policy)
        else:
            total_points += dropout_weight * indicators[one_year_dropout_rate]
            self.weights["one_year_dropout_rate"] = dropout_weight

        #8. Graduation with early college/career credentials
        credential_weight = self.weights["percent_graduating_with_creds"] + (
            policy.percent_graduating_with_creds * base_weight)
        if credential_weight > 0 and not indicators[credentials]:
            self.reassign_to_growth(credential_weight, indicators, policy)
        else:
            total_points += credential_weight * indicators[credentials]
            self.weights["percent_graduating_with_creds"] = credential_weight

        #9. 5 Essentials Survey
        survey_weight = self.weights["five_essentials_survey"] + (
            policy.five_essentials_survey * base_weight)
        if survey_weight > 0 and not indicators[survey]:
            self.reassign_to_growth(survey_weight, indicators, policy)
        else:
            total_points += survey_weight * indicators[survey]
            self.weights["five_essentials_survey"] = survey_weight

        #10. Data Quality Index
        quality_weight = self.weights["data_quality_index_score"] + (
            policy.data_quality_index_score * base_weight)
        if quality_weight > 0 and not indicators[data_quality]:
            self.reassign_to_growth(quality_weight, indicators, policy)
        else:
            total_points += survey_weight * indicators[data_quality]
            self.weights["data_quality_index_score"] = quality_weight


        return total_points


    def reassign_readiness_weight(self, weight, indicators, policy):
        non_assessment_count = 0
        for i in indicators: #subset to proper indicators
            if i and policy.i > 0:
                non_assessment_count += 1
        reassigned_weight = 1 / non_assessment_count if (
            non_assessment_count > 0 else 1 / 9)
        for i in indicators: #subset to proper indicators
            self.weights[i] = self.weights[i] + reassigned_weight

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
        reassign_weight = 1 / rel_weight_total if rel_weight_total > 0 else 1 / 4
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
        weight_reassignment = {"grade_11_sat_3yr_cohort_growth": 2,
                               "grade_11_sat_growth_ebrw": 1,
                               "grade_11_sat_growth_math": 1,
                               "grade_10_psat_annual_growth_ebrw": 1,
                               "grade_10_psat_annual_growth_math": 1,
                               "grade_9_psat_cohort_growth": 2}
        rel_weight_total = 0
        for indicator, rel_weight in weight_reassignment.items():
            if policy.indicator > 0:
                rel_weight_total += rel_weight
        reassigned_weight = weight * (1 / rel_weight_total) if (
            rel_weight_total > 0 else 1 / 8)
        points = 0
        for i in indicators: #adjust this to reflect data structure
            if policy.i > 0 and not i:
                points += reassign_weights2(args)
            else:
                points += adj_base_weight * weight_reassignment[i] * i
        return points