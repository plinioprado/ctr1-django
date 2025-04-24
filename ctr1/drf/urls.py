""" Parameters to redirect DRF Request objects from drf.urls to ledger1.drf.views """

from django.urls import path
from . import views_login
from . import views_admin

urlpatterns = [
    path("admin/<str:param>", views_admin.view),
    path("admin/<str:param>/<str:record_id>", views_admin.view),
    path("login", views_login.view),
]
