'''
bias_score.py
-----------
Calculate the bias score of an SQRP. For more information on how the bias score
was developed, please see "bias_score_dev.pdf" under "core/docs."
'''
import io
import base64
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
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
    Calculates the bias score associated with an SQRP policy from a regression
    of SQRP points on percentage low-income students, percentage
    English-language learner students, and percentage of special education
    students. Then plots the regression through a call to create_reg_plots.

    Inputs:
        df (pd.DataFrame): enrollment information summarizing the percentages of
            students who are low-income, English language learners, or in
            special education

    Returns:
        (int): the bias score
        (str): a base64-encoded string containing the regression plots as a
               single SVG image
    '''
    #Filter schools
    df = df[df["sqrp_points"] != 0]
    df = df.dropna()
    if not len(df):
        return "N/A"

    #Run the regression
    X = df[["percent_low_income", "percent_english_learners", 
            "percent_special_ed"]]
    y = df["sqrp_points"]
    reg = LinearRegression().fit(X, y)
    reg_plots = create_reg_plots(df)

    return round(100 * reg.score(X, y), 0), reg_plots


def create_reg_plots(df):
    '''
    Generate visualizations for the given dataframe. Creates one
    figure with three plots: percent low income, percent English learners,
    and percent special education, all vs. SQRP points. Adds a linear
    regression line for each.

    Inputs:
        df (pd.DataFrame): Data generated from calculate_bias_score functions

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

    plt.tight_layout()
    reg_plots = fig_to_base64(plt)
    plt.close("all")
    return reg_plots


def create_histogram(ratings_lst):
    '''
    Creates a histogram for the distribution of schools across levels and then
    saves that histogram as an SVG file called "level_dist.svg" in the project
    directory.

    Inputs:
        ratings_lst (list): a list of all the ratings

    Returns:
        None
    '''
    sns.set()

    fig = plt.gcf()
    fig.set_size_inches(7, 4)
    colors = ["#B875C3", "#A147AF", "#7C178C", "#60126D", "#450D4E", "#000000"]
    order = ["Level 1+", "Level 1", "Level 2+", "Level 2", "Level 3",
             "Inability to Rate"]
    sns.countplot(ratings_lst, order=order, palette=colors)
    plt.ylabel("Number of Schools")

    plt.tight_layout()
    level_histogram = fig_to_base64(plt)
    plt.close("all")
    return level_histogram


def fig_to_base64(fig):
    '''
    Converts a matplotlib figure into a base64-encoded string bearing an
    SVG image.
    
    Credits: https://stackoverflow.com/questions/49015957/how-to-get-python-graph-output-into-html-webpage-directly

    Inputs:
        fig (matplotlib.pyplot): the figure to encode

    Returns:
        (str): the encoded string
    '''
    img = io.BytesIO()
    fig.savefig(img, format='svg', bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())
