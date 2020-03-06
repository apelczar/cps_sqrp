#----------------
#
# Calculate the bias score of a policy
# For more information on how the bias score
# was developed, see <file name>
#
#----------------

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt

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
    create_plots(df, reg)

    return round(100 * reg.score(X, y), 0)


def create_plots(df, regression):
    return
    sns.set()

    intercept = regression.intercept_
    beta1 = regression.coef_[0]
    beta2 = regression.coef_[1]
    beta3 = regression.coef_[2]

    #x = np.linspace(0, 1, 100)
    #fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, sharey=True)
    #sns.relplot(x="percent_low_income", y="sqrp_points", data=df, ax=ax1)
    #sns.lineplot(x, x*beta1 + intercept, ax=ax1)
    #sns.relplot(x="percent_english_learners", y="sqrp_points", data=df, ax=ax2)
    #sns.lineplot(x, x*beta2 + intercept, ax=ax2)
    #sns.relplot(x="percent_special_ed", y="sqrp_points", data=df, ax=ax3)
    #sns.lineplot(x, x*beta3 + intercept, ax=ax3)


    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, sharey=True)
    sns.regplot(x="percent_low_income", y="sqrp_points", data=df, ax=ax1)
    ax1.set(xlabel="Percent Low Income", ylabel="SQRP Points")
    sns.regplot(x="percent_english_learners", y="sqrp_points", data=df, ax=ax2)
    ax2.set(xlabel="Percent English Learners", ylabel="")
    sns.regplot(x="percent_special_ed", y="sqrp_points", data=df, ax=ax3)
    ax3.set(xlabel="Percent Special Education", ylabel="")
