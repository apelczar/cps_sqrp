'''
point_calculator.py
-----------
Counts the number of points earned by a school under a given SQRP model.
These points are used to determine the final level/ranking of the school. 
'''
from core.models.reassignments import NON_ASSESSMENT_REASSIGNMENT
from core.models.indicators import (ATTAINMENT_INDICATORS, 
                                    ASSESSMENT_INDICATORS,
                                    PRIORITY_GROUP_INDICATORS)

class PointCalculator():
    def __init__(self, school, record, policy):
        self.school = school
        self.indicators = record
        self.policy = policy
        self.points = self.calculate_points()

    def calculate_points(self):
        '''
        Calculate the number of points earned under the user's policy.

        Inputs:
            indicators: the school's record from the SQRP points database
            policy: an SQRP object
            base_weight: the base weight for the given policy

        Returns:
            the points that the school earned under the policy
        '''

        total_points = 0

        for indicator, function in NON_ASSESSMENT_REASSIGNMENT:
            total_points += self.calculate_ind_points(indicator, function)

        #Assessment indicators
        #Calculate priority group weights and points
        if self.policy.priority_group_sat_growth > 0:
            total_points += self.calculate_priority_group_points()

        #Growth indicators: Calculate and reassign weights as needed,
        #and calculate points
        total_points += self.calculate_growth_points()

        #Additional inputs: Calculate and reassign weights as needed,
        #and calulcate points
        total_points += self.calculate_add_input_points()

        #Check that all weight has been reassigned
        #If it hasn't inflate currently calculated points according to their
        #relative weight
        total_weight = round(sum(self.school.weights.values()), 2)
        if total_weight != 1 and total_weight != 0:
            total_points = self.inflate_weights(total_weight, total_points)

        #add 0.001 to handle errors due to floating point values
        return total_points + 0.001


    def calculate_ind_points(self, indicator, reassignment_function):
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

        Returns:
            (float) the points for that indicator
        '''

        ind_weight = self.school.weights[indicator] + (
            self.policy.relative_weights[indicator] * self.policy.base_weight)
        if self.policy.relative_weights[indicator] and self.indicators[indicator]:
            self.school.weights[indicator] = ind_weight
            return ind_weight * self.indicators[indicator]
        elif ind_weight:
            reassignment_function(self.school, ind_weight,
                                  self.indicators, self.policy)
            self.school.weights[indicator] = 0
        return 0


    def calculate_priority_group_points(self):
        '''
        Calculates the points for the 11th grade SAT priority groups.
        Also reassigns weight as needed.

        Returns:
            (float) the points for the priority group category

        '''

        priority_num_weight = (self.policy.relative_weights["priority_group_sat_growth"] * 
                               self.policy.base_weight) / 4
        priority_points = 0
        priority_group_weight = 0
        for group in PRIORITY_GROUP_INDICATORS:
            if self.indicators[group]:
                priority_points += self.indicators[group] * priority_num_weight
                priority_group_weight += priority_num_weight
            else:
                self.school.weights["grade_11_sat_3yr_cohort_growth"] = (
                    self.school.weights["grade_11_sat_3yr_cohort_growth"] +
                    priority_num_weight)
        self.school.weights["priority_group_sat_growth"] = priority_group_weight
        return priority_points


    def calculate_growth_points(self):
        '''
        Calculates the weights for all SAT growth measures other than
        priority groups, and the points for all these indicators

        Returns:
            (float) the number of points for all SAT growth measures
        '''

        points = 0
        #Get base numerical weights
        for indicator in ASSESSMENT_INDICATORS:
            self.school.weights[indicator] = self.school.weights[indicator] + (
            self.policy.relative_weights[indicator] * self.policy.base_weight)

        grade_level_growth_count = 0
        weight_to_reassign = 0
        for measure in ASSESSMENT_INDICATORS[1:]:
            if self.policy.relative_weights[measure] and self.indicators[measure]:
                grade_level_growth_count += 1
            else:
                weight_to_reassign += self.school.weights[measure]
                self.school.weights[measure] = 0

        #If all grade-level growth measures are missing and/or not included,
        #give any weight for them to cohort growth. If cohort growth is
        #also missing or not included, reassignment fails.
        if not grade_level_growth_count:
            if (self.indicators["grade_11_sat_3yr_cohort_growth"] and
            self.policy.grade_11_sat_3yr_cohort_growth):
                self.school.weights["grade_11_sat_3yr_cohort_growth"] = (
                self.school.weights["grade_11_sat_3yr_cohort_growth"] +
                weight_to_reassign)
                points = (self.indicators["grade_11_sat_3yr_cohort_growth"] *
                         self.school.weights["grade_11_sat_3yr_cohort_growth"])
            else:
                self.school.weights["grade_11_sat_3yr_cohort_growth"] = 0
            return points


        #If there is weight to reassign among one-year growth indicators:
        reassigned_weight = weight_to_reassign / grade_level_growth_count

        #calculate 3-yr growth points or reassign its weight
        if (self.policy.grade_11_sat_3yr_cohort_growth and
            self.indicators["grade_11_sat_3yr_cohort_growth"]):
            points += (self.school.weights["grade_11_sat_3yr_cohort_growth"] *
                       self.indicators["grade_11_sat_3yr_cohort_growth"])
        else:
            reassigned_weight += self.school.weights[
                "grade_11_sat_3yr_cohort_growth"] / grade_level_growth_count
            self.school.weights["grade_11_sat_3yr_cohort_growth"] = 0

        #Reallocate weight and calculate points
        for measure in ASSESSMENT_INDICATORS[1:]:
            if self.policy.relative_weights[measure] and self.indicators[measure]:
                self.school.weights[measure] = (self.school.weights[measure] +
                                                reassigned_weight)
                points += self.school.weights[measure] * self.indicators[measure]
        return points


    def calculate_add_input_points(self):
        '''
        Calculates weight for additional inputs (attainment scores)

        Returns:
            the points for all additional inputs
        '''

        points = 0
        weight_to_reassign = 0
        rel_weight_total = 0
        for item in ATTAINMENT_INDICATORS:
            item_weight = (self.policy.relative_weights[item] *
                           self.policy.base_weight)
            if not self.indicators[item]:
                weight_to_reassign += item_weight
            else:
                rel_weight_total += self.policy.relative_weights[item]
                self.school.weights[item] = item_weight

        if not rel_weight_total:
            return points

        reassigned_weight = weight_to_reassign / rel_weight_total

        for item in ATTAINMENT_INDICATORS:
            if self.indicators[item] and self.school.weights[item]:
                self.school.weights[item] = (self.school.weights[item] +
                                             reassigned_weight)
                points += self.indicators[item] * self.school.weights[item]
        return points


    def inflate_weights(self, weight, points):
        '''
        Inflates weights and adjusts point total, proportional to
        relative weights, in the case that the total weight does not equal 1

        Inputs:
            weight: the total weight so far
            points: the number of points so far

        Returns:
            (float) the adjusted number of points
        '''
        used_rel_weight_total = 0
        for indicator, wt in self.school.weights.items():
            if wt and indicator != "priority_group_sat_growth":
                used_rel_weight_total += self.policy.relative_weights[indicator]
        if not used_rel_weight_total:
            return points / weight
        inflation_base = (1 - weight) / used_rel_weight_total
        for indicator in self.school.weights:
            if (self.school.weights[indicator] and indicator != 
                "priority_group_sat_growth"):
                added_weight = (inflation_base *
                                self.policy.relative_weights[indicator])
                points += self.indicators[indicator] * added_weight
                self.school.weights[indicator] = (self.school.weights[indicator]
                                                  + added_weight)
        return points
