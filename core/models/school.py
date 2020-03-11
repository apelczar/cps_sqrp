'''
school.py
---------
Represents a CPS school assigned an SQRP rating.
'''
import os
from decimal import Decimal, ROUND_HALF_UP
from core.models.indicators import ALL_INDICATORS
from core.models.point_calculator import PointCalculator


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
        self.latitude = record["school_latitude"]
        self.longitude = record["school_longitude"]
        self.cps_rating = record["current_sqrp_rating"]
        self.weights = {k:0 for k in ALL_INDICATORS}
        points = PointCalculator(self, record, policy).points
        self.sqrp_points = float(Decimal(str(points)).quantize(Decimal("0.1"),
                                 rounding=ROUND_HALF_UP))
        self.sqrp_rating = self.assign_rating(self.sqrp_points)


    def __repr__(self):
        return "{}, ID {}: {} points, rating of {}".format(self.name, self.id,
            self.sqrp_points, self.sqrp_rating)


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
