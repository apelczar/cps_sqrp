'''
urls.py
--------------
Routing used in the Django web app.
'''

from django.urls import path
from sqrp import views

urlpatterns = [
    path("", views.home, name="home"),
]