"""
Parameters to redirect DRF Request objects from drf.urls to document views
"""

from django.urls import path
from . import views_inv2
from . import views_banstat2

urlpatterns = [
    path("inv2/", views_inv2.view),
    path("inv2/<str:num>/", views_inv2.view),
    path("banstat/", views_banstat2.view),
    path("banstat/<str:acc>/", views_banstat2.view),
]
