import sqlite3

enrollment_q = """
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
"""

def test_table_setup():

    con = sqlite3.connect("db.sqlite3")
    u = con.cursor()
    u.execute(enrollment_q)
    return None
