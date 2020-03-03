#----------------
#
# Calculate the bias score of a policy
#
#----------------

import pandas as pd
from sklearn.linear_model import LinearRegression

def calculate_bias_score(df):
    #df["percent_low_income"] = (df["student_count_low_income"] / 
    #                            df["student_count_total"])
    #df["percent_english_learners"] = (df["student_count_english_learners"] / 
    #                                  df["student_count_total"])
    #df["percent_special_ed"] = (df["student_count_special_ed"] / 
    #                            df["student_count_total"])

    #Filter schools - check this is sufficient
    df = df[df["sqrp_points"] != 0]
    df = df.dropna()

    #Run the regression
    X = df[["percent_low_income", "percent_english_learners", 
            "percent_special_ed"]]
    y = df["sqrp_points"]
    reg = LinearRegression().fit(X, y)

    return reg.score(X, y)