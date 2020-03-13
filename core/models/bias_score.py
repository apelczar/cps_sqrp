#----------------
#
# Calculate the bias score of a policy
# For more information on how the bias score
# was developed, see <file name>
#
#----------------

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

BIAS_SCORE_EXPLANATION = '''
    The bias score measures how well the demographics of schools align with the 
    points they earn under the SQRP. It ranges from 0 to 100. Lower scores 
    represent less bias: a 0 means that the demographics of a school tells us 
    nothing about its point total, while a 100 means that we can perfectly 
    predict a school's point total with only its demographic information. The 
    demographic measures used in calculating the bias score are the percent of 
    students who are low income, special education, and English language 
    learners. From a statistical perspective, the bias score is the R^2 value, 
    in integer form, of a linear regression model with SQRP points as the 
    dependent variable and the three demographic measures above as the 
    independent variables. For reference, the bias score of the 2018-2019 
    SQRP policy is 53.
    '''

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
        saves a file called "bias_score_viz.svg"
    '''

    sns.set()

    colors = ["#00956E", "#8A1A9C", "#EE7624"]
    _, (ax1, ax2, ax3) = plt.subplots(ncols=3, sharey=True)
    sns.regplot(x="percent_low_income", y="sqrp_points", data=df, ci=None,
                color=colors[0], ax=ax1)
    ax1.set(xlabel="Low Income", ylabel="SQRP Points", ylim=(0,5))
    sns.regplot(x="percent_english_learners", y="sqrp_points", data=df, ci=None,
                color=colors[1], ax=ax2)
    ax2.set(xlabel="English Learners", ylabel="", ylim=(0,5))
    sns.regplot(x="percent_special_ed", y="sqrp_points", data=df, ci=None,
                color=colors[2], ax=ax3)
    ax3.set(xlabel="Special Education", ylabel="", ylim=(0,5))

    plt.savefig("./sqrp/static/img/bias_score_viz.svg")
    plt.close("all")


def create_histogram(ratings_lst):
    '''
    Create a histogram for the distribution of schools across levels.

    Inputs:
        ratings_lst: a list of all the ratings

    Returns:
        saves a file called "level_dist.svg"
    '''
    sns.set()

    fig = plt.gcf()
    fig.set_size_inches(7, 4)
    colors = ["#B875C3", "#A147AF", "#7C178C", "#60126D", "#450D4E", "#000000"]
    order = ["Level 1+", "Level 1", "Level 2+", "Level 2", "Level 3",
             "Inability to Rate"]
    sns.countplot(ratings_lst, order=order, palette=colors)
    plt.ylabel("Number of Schools")
    plt.savefig("./sqrp/static/img/level_dist.svg",bbox_inches='tight')
    plt.close("all")
