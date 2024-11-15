""" Parameters to redirect DRF Request objects from drf.urls to ledger1.drf.views """

from django.urls import path
from . import views_account
from . import views_transaction
from . import views_report
from . import views_reset
from . import views_banstat2
from . import views_inv2
from . import views_pmt

urlpatterns = [
    path("accounts/", views_account.view),
    path("accounts/<str:acc>", views_account.view),
    path("report/<str:name>", views_report.view),
    path("reset/", views_reset.view),
    path("transactions/", views_transaction.view),
    path("transactions/<int:num>", views_transaction.view),
    path("doc/banstat/", views_banstat2.view),
    path("doc/banstat/<str:acc>/", views_banstat2.view),
    path("doc/inv2/", views_inv2.view),
    path("doc/inv2/<str:num>/", views_inv2.view),
    path("doc/pmt/", views_pmt.view),
    path("doc/pmt/<str:num>/", views_pmt.view),
]
