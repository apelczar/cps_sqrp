'''
views.py
--------------
Relays SQRP models created in the web interface to the backend for processing
and then returns the rendered results back to the interface.
'''

from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .forms import SQRPModelConfigForm

import sys
import json
from core import analyzesqrp
from core.models.sqrp import SQRP, DEFAULT_RELATIVE_WEIGHTS
from core.models.indicators import ALL_INDICATORS
from core.models.bias_score import BIAS_SCORE_EXPLANATION

def home(request):
    '''
    Renders the home page/main landing page of the application. When the page
    first loads following a GET request, the default relative weights from the
    Chicago Public Schools 2018-2019 school year are used.  Subsequent POST
    requests by the user update the page with user-selected weights.

    Inputs:
        (django.HttpRequest): the HTTP request for the home page

    Returns:
        (django.HttpResponse): the HttpResponse with the rendered "home.html"
                               template
    '''
    try:
        if request.method == "POST":
            weights = request.POST
        else:
            weights = DEFAULT_RELATIVE_WEIGHTS
            
        form = SQRPModelConfigForm(weights)
        policy = SQRP({i : int(weights[i]) for i in ALL_INDICATORS})
        results = analyzesqrp.calculate_sqrp_scores(policy)

        schools_as_dict = [vars(s) for s in results[0]]
        bias_score = results[1]
        ratings_histogram = results[2]
        reg_plots = results[3]

    except Exception as e:
        print('Exception occurred:', e)

    return render(request, 'home.html', context=
    {
        'form': form,
        'schools': schools_as_dict,
        'bias_score': "{:.0f}".format(bias_score),
        'bias_score_explanation': BIAS_SCORE_EXPLANATION,
        'ratings_histogram': ratings_histogram,
        'reg_plots': reg_plots
    })
