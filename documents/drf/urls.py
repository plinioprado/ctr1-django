"""
Parameters to redirect DRF Request objects from drf.urls to document views
"""

from django.urls import path
from . import views_admin
from . import views_inv2
#from . import views_test

urlpatterns = [
    path("admin/<str:op>/", views_admin.view),
    path("inv2/", views_inv2.view),
    path("inv2/<str:num>/", views_inv2.view),
]
