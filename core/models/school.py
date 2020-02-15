###############
#
# School class for output
#
###############

'''
To add to SQRP object:
a method that returns the "base weight"
something like this:

def calculate_base_weight(self):
    weight_total = 0
    for v in self.vars():
        weight_totals += v
    return 1 / weight_totals
'''

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

    def calculate_rating(self, sqrp_points, policy):
        '''
        Calculate a rating under the user's policy
        Inputs:
            sqrp_points: the school's record from the SQRP points database
            policy: an SQRP object

        Returns:
            the points that the school earned under the policy
        '''
        base = policy.calculate_base_weight()
        total_points = 0
        total_points += (sqrp_points[11th_grade_pts] - penalty) * (
            policy.grade11_overall * base)
        for group in priority_groups:
            if group == 0:
                total_points += (sqrp_points[11th_grade_pts] - penalty) * (
                policy.priority_groups * base / 4)
            else:
                total_points += (sqrp_points[group_pts] - penalty) * (
                    policy.priority_groups * base / 4)
        #additional inputs here

        #CHECK THESE BOUNDARIES. CPS website currently under maintenance
        #so I can't load the handbook
        if total_points > 0 and total_points <= 2:
            sqrp_rating = "Level 3"
        elif total_points > 2 and total_points <= 2.9:
            sqrp_rating = "Level 2"
        elif total_points > 2.9 and total_points <= 3.5:
            sqrp_rating = "Level 2+"
        elif total_points > 3.5 and total_points <= 3.9:
            sqrp_rating = "Level 1"
        elif sqrp_rating > 3.9:
            sqrp_rating = "Level 1+"
        #use total_points = 0 to indicate a problem

        return total_points
