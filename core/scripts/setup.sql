CREATE TABLE enrollment
	(school_id varchar(10),
		percent_low_income decimal,
		percent_english_learners decimal,
		percent_special_ed decimal,
	constraint pk_enrollment primary key (school_id)
);


CREATE TABLE sqrp
	(school_id varchar(10),
		school_name varchar(50),
		grade_11_sat_3yr_cohort_growth decimal,
		grade_11_sat_growth_ebrw decimal,
		grade_11_sat_growth_math decimal,
		grade_10_psat_annual_growth_ebrw decimal,
		grade_10_psat_annual_growth_math decimal,
		grade_9_psat_cohort_growth decimal,
		percent_students_college_ready decimal,
		avg_daily_attendance_rate decimal,
		freshmen_on_track_rate decimal,
		four_year_cohort_graduation_rate decimal,
		one_year_dropout_rate decimal,
		percent_graduating_with_creds decimal,
		college_enrollment_rate decimal,
		college_persistence_rate decimal,
		five_essentials_survey decimal,
		data_quality_index_score decimal,
		aa_sat_growth decimal,
		hispanic_sat_growth decimal,
		el_sat_growth decimal,
		dl_sat_growth decimal,
		current_sqrp_rating decimal,
		school_latitude decimal,
		school_longitude decimal,
		attainment_psat_grade_9_school decimal,
		attainment_psat_grade_10 decimal,
		attainment_sat_grade_11_school decimal,
		constraint pk_sqrp primary key (school_id)
);



