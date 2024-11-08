""" Parameters to redirect DRF Request objects from drf.urls to ledger1.drf.views """

from django.urls import path
from . import views_account
from . import views_transaction
from . import views_report
from . import views_reset

urlpatterns = [
    path("accounts/", views_account.view),
    path("accounts/<str:acc>", views_account.view),
    path("report/<str:name>", views_report.view),
    path("reset/", views_reset.view),
    path("transactions/", views_transaction.view),
    path("transactions/<int:num>", views_transaction.view),
]
