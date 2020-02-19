class SQRP(object):
    def __init__(self, relative_weights={}):
        '''
        Instantiates a new School Quality Rating Policy (SQRP) model.

        Inputs:
            relative_weights (dict<string, int>): a dictionary with indicator
                names as keys and relative integer weights (0-10) as values.
                Defaults to empty, in which case the calculated weights from
                the most recent CPS year (2018-19) are used.

        Outputs:
            (SQRP): the model
        '''
        self.__relative_weights = relative_weights

    @property
    def grade_11_sat_3yr_cohort_growth(self):
        '''
        The relative weight for indicator 1 of 17: the overall SAT growth rate
        for a school. Defaults to 6.
        '''
        return self.__relative_weights.get("grade_11_sat_3yr_cohort_growth", 6)

    @property
    def priority_group_sat_growth(self):
        '''
        The relative weight for indicator 2 of 17: the SAT growth rate for
        students in the four priority groups. Defaults to 6.
        
        Priority groups include African American students, Hispanic students,
        English Learners and Diverse Learners. If there are fewer than 30
        students in the priority group, the indicator is not
        used and the weight is reallocated to the SAT Cohort growth indicator.
        '''
        return self.__relative_weights.get("priority_group_sat_growth", 6)

    @property
    def grade_11_sat_growth_ebrw(self):
        '''
        The relative weight for indicator 3 of 17: the annual SAT EBRW
        (Evidence-Based Reading and Writing) section growth rate for the cohort
        of current 11th graders. Defaults to 1.

        The growth rate is calculated by comparing the average spring-to-spring
        scale score growth of 11th graders on the SAT EBRW section compared to
        the average national growth for schools with the same pretest score. The
        school is assigned a percentile representing where it would fall on the
        national distribution. 
        '''
        return self.__relative_weights.get("grade_11_sat_growth_ebrw", 1)

    @property
    def grade_11_sat_growth_math(self):
        '''
        The relative weight for indicator 4 of 17: the annual SAT math section
        growth rate for the cohort of current 11th graders. Defaults to 1.

        The growth rate is calculated by comparing the average spring-to-spring
        scale score growth of 11th graders on the SAT math section compared to
        the average national growth for schools with the same pretest score. The
        school is assigned a percentile representing where it would fall on the
        national distribution. 
        '''
        return self.__relative_weights.get("grade_11_sat_growth_math", 1)

    @property
    def grade_10_psat_annual_growth_ebrw(self):
        '''
        The relative weight for indicator 5 of 17: the annual PSAT EBRW
        (Evidence-Based Reading and Writing) section growth rate for the cohort
        of current 10th graders. Defaults to 1.

        The growth rate is calculated by comparing the average spring-to-spring
        scale score growth of 10th graders on the PSAT EBRW section compared to
        the average national growth for schools with the same pretest score. The
        school is assigned a percentile representing where it would fall on the
        national distribution. 
        '''
        return self.__relative_weights.get("grade_10_psat_annual_growth_ebrw", 1)

    @property
    def grade_10_psat_annual_growth_math(self):
        '''
        The relative weight for indicator 6 of 17: the annual PSAT math section
        growth rate for the cohort of current 10th graders. Defaults to 1.

        The growth rate is calculated by comparing the average spring-to-spring
        scale score growth of 10th graders on the PSAT math section compared to
        the average national growth for schools with the same pretest score. The
        school is assigned a percentile representing where it would fall on the
        national distribution. 
        '''
        return self.__relative_weights.get("grade_10_psat_annual_growth_math", 1)

    @property
    def grade_9_psat_cohort_growth(self):
        '''
        The relative weight for indicator 7 of 17: the one-year PSAT growth rate
        for the cohort of current 9th graders. Defaults to 6.
        
        The growth rate is calculated from the spring PSAT composite scale score
        minus the average expected PSAT Composite scale score for 9th grade.
        '''
        return self.__relative_weights.get("grade_9_psat_cohort_growth", 2)

    @property
    def percent_students_college_ready(self):
        '''
        The relative weight for indicator 8 of 17: the percentage of students in
        the 9th, 10th, and 11th grades meeting or exceeding combined College
        Readiness Benchmarks established by the College Board. Defaults to 6.
        '''
        return self.__relative_weights.get("percent_students_college_ready", 6)

    @property
    def avg_daily_attendance_rate(self):
        '''
        The relative weight for indicator 9 of 17: the average daily attendance
        rate of the school. Defaults to 6.
        
        The attendance rate is adjusted for students with qualifying medically
        fragile conditions, early graduation for 8th and 12th graders,
        transportation adjustments, and each school’s two lowest attendance days
        only if the adjustment would improve the school's rate.
        '''
        return self.__relative_weights.get("avg_daily_attendance_rate", 6)

    @property
    def freshmen_on_track_rate(self):
        '''
        The relative weight for indicator 10 of 17: the percentage of students
        earning five or more credits and failing no more than 0.5 courses in a
        core subject during their 9th grade year. Defaults to 6.
        '''
        return self.__relative_weights.get("freshmen_on_track_rate", 6)

    @property
    def four_year_cohort_graduation_rate(self):
        '''
        The relative weight for indicator 11 of 17: the percentage of students
        who were first-time freshmen four years prior who have graduated.
        Defaults to 6.
        '''
        return self.__relative_weights.get("four_year_cohort_graduation_rate", 6)

    @property
    def one_year_dropout_rate(self):
        '''
        The relative weight for indicator 12 of 17: the percentage of students
        in grades 9-12 dropping out during the year. Defaults to 3.
        '''
        return self.__relative_weights.get("one_year_dropout_rate", 3)

    @property
    def percent_graduating_with_creds(self):
        '''
        The relative weight for indicator 13 of 17: the percentage of graduating
        students who have received early college or career credentials. Defaults
        to 3.
        
        Eligible credentials include: at least one credit from an approved early
        college course, a 3+ on an AP exam, a 4+ on an IB exam, the State Seal
        of Biliteracy, or an approved career certification
        '''
        return self.__relative_weights.get("percent_graduating_with_creds", 3)

    @property
    def college_enrollment_rate(self):
        '''
        The relative weight for indicator 14 of 17: the percentage of students
        enrolled in a two- or four-year college in the fall or spring after
        graduation from high school. Defaults to 3.
        '''
        return self.__relative_weights.get("college_enrollment_rate", 3)

    @property
    def college_persistent_rate(self):
        '''
        The relative weight for indicator 15 of 17: the percentage of students
        enrolled in a two- or four-year college in the fall or spring after
        graduation from high school that remain enrolled in college the
        following fall. Defaults to 3.
        '''
        return self.__relative_weights.get("college_persistent_rate", 3)

    @property
    def five_essentials_survey(self):
        '''
        The relative weight for indicator 16 of 17: the overall rating of the
        school on the "My School, My Voice 5 Essentials" survey administered in
        the spring to students and teachers. Defaults to 3.

        Schools must have a 50 percent response rate to receive a survey rating.
        The rating is determined using data from all five essentials, or
        from whatever combination of essentials for which the school has
        sufficient data.
        '''
        return self.__relative_weights.get("five_essentials_survey", 3)

    @property
    def data_quality_index_score(self):
        '''
        The relative weight for indicator 17 of 17: the percentage of data
        quality indicators that are correct in CPS data systems. Defaults to 3.
        '''
        return self.__relative_weights.get("data_quality_index_score", 3)

    def calculate_base_weight(self):
        '''
        Use the relative weights of all indicators to calculate the numerical
        weight corresponding to a relative weight of 1. Defaults to 1/60, the
        base weight for the default relative weights.

        Returns: float, with a value 0 - 1
        '''
        if not self.__relative_weights: #if using default weights
            return 1/60

        total = 0
        for weight in self.__relative_weights.values():
            total += weight
        return 1 / total