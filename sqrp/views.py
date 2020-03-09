from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .forms import SQRPModelConfigForm

import sys
import json
sys.path.append('..')
from core import analyzesqrp
from core.models.indicators import INDICATOR_LABEL_DICT
from core.models.sqrp import DEFAULT_RELATIVE_WEIGHTS

def home(request):
    if request.method == "POST":
        form = SQRPModelConfigForm(request.POST)
        try:
            processed = process_user_input(request.POST)
            (schools, bias_score) = analyzesqrp.calculate_sqrp_scores(processed)
        except Exception as e:
            print('Exception caught', e)   
    else:
        form = SQRPModelConfigForm(DEFAULT_RELATIVE_WEIGHTS)
        (schools, bias_score) = analyzesqrp.calculate_sqrp_scores(DEFAULT_RELATIVE_WEIGHTS)

    return render(request, 'home.html', context=
    {
        'form': form,
        'schools': json.dumps(schools) if schools else [],
        'bias_score': bias_score
    })


def process_user_input(query_dict):
    processed = {}
    for k in query_dict:
        if k in INDICATOR_LABEL_DICT.values():
            processed[k] = query_dict[k]
    return processed