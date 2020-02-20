CREATE TABLE enrollment
	(school_id varchar(10),
	student_count_total int,
	student_count_low_income int,
	student_count_special_ed int,
	student_count_english_learners int,
	student_count_black int,
	student_count_hispanic int,
	student_count_white int,
	student_count_asian int,
	student_count_native_american int,
	student_count_other_ethnicity int,
	student_count_asian_pacific int,
	student_count_multi int,
	student_count_hawaiian_pacific int,
	student_count_ethnicity_not int,
	bilingual_services BIT,
	refugee_services BIT,
	title_1_eligible BIT,
	constraint pk_enrollment primary key (school_id)
);

CREATE TABLE location
	(school_id varchar(10),
		school_latitude decimal,
		school_longitude decimal,
		constraint pk_location primary key (school_id)
);

CREATE TABLE sqrp
	(school_id varchar(10),
		school_name varchar(50),
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
		constraint pk_sqrp primary key (school_id)
);



