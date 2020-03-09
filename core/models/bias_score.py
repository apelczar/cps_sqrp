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
    '''
    Calculates the bias score associated with an SQRP policy

    Inputs:
        df: a pandas dataframe with enrollment info (% low income,
        % English learners, and % special education)

    Returns:
        (int) the bias score
        also generates plots through a call to create_plots
    '''

    #Filter schools
    df = df[df["sqrp_points"] != 0]
    df = df.dropna()

    #Run the regression
    X = df[["percent_low_income", "percent_english_learners", 
            "percent_special_ed"]]
    y = df["sqrp_points"]
    reg = LinearRegression().fit(X, y)
    create_plots(df)

    return round(100 * reg.score(X, y), 0)


def create_plots(df):
    '''
    Generate visualizations for the given dataframe. Creates one
    figure with three plots: percent low income, percent English learners,
    and percent special education, all vs. SQRP points. Adds a linear
    regression line for each.

    Inputs:
        df: pandas dataframe from calculate_bias_score functions

    Returns:
        saves a file called "bias_score_viz.svg" in folder core/plots
    '''

    sns.set()

    colors = ["#00956E", "#8A1A9C", "#EE7624"]
    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, sharey=True)
    sns.regplot(x="percent_low_income", y="sqrp_points", data=df, ci=None,
                color=colors[0], ax=ax1)
    ax1.set(xlabel="Percent Low Income", ylabel="SQRP Points", ylim=(0,5))
    sns.regplot(x="percent_english_learners", y="sqrp_points", data=df, ci=None,
                color=colors[1], ax=ax2)
    ax2.set(xlabel="Percent English Learners", ylabel="", ylim=(0,5))
    sns.regplot(x="percent_special_ed", y="sqrp_points", data=df, ci=None,
                color=colors[2], ax=ax3)
    ax3.set(xlabel="Percent Special Education", ylabel="", ylim=(0,5))

    plt.savefig("../plots/bias_score_viz.svg")