""" Parameters to redirect DRF Request objects from drf.urls to ledger1.drf.views """

from django.urls import path
from . import views_account
from . import views_transaction
from . import views_report

urlpatterns = [
    path("account/", views_account.view),
    path("transaction/", views_transaction.view),
    path("report/<str:name>/", views_report.view),
]
