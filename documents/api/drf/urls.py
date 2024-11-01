"""
Parameters to redirect DRF Request objects from drf.urls to document views
"""

from django.urls import path
from . import views_admin

urlpatterns = [
    path("admin/<str:op>", views_admin.view),
]
