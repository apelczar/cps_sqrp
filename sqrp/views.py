from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .forms import SQRPModelConfigForm

import sys
import json
#sys.path.append('..')
from core import analyzesqrp
from core.models.sqrp import SQRP, DEFAULT_RELATIVE_WEIGHTS
from core.models.indicators import ALL_INDICATORS
from core.models.bias_score import BIAS_SCORE_EXPLANATION

def home(request):
    try:
        if request.method == "POST":
            weights = request.POST
        else:
            weights = DEFAULT_RELATIVE_WEIGHTS
            
        form = SQRPModelConfigForm(weights)
        policy = SQRP({i : int(weights[i]) for i in ALL_INDICATORS})
        (schools, bias_score) = analyzesqrp.calculate_sqrp_scores(policy)
        schools_as_dict = [vars(s) for s in schools]

    except Exception as e:
        print('Exception occurred:', e)

    return render(request, 'home.html', context=
    {
        'form': form,
        'schools': schools_as_dict,
        'bias_score': "{:.0f}".format(bias_score),
        'bias_score_explanation': BIAS_SCORE_EXPLANATION
    })
