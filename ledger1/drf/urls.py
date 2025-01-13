""" Parameters to redirect DRF Request objects from drf.urls to ledger1.drf.views """

from django.urls import path
from . import views_account
from . import views_transaction
from . import views_report
from . import views_banstat2
#from . import views_inv2
from . import views_eft
from . import views_login
from . import views_admin
from . import views_document

urlpatterns = [
    path("accounts", views_account.view),
    path("accounts/<str:acc>", views_account.view),
    path("admin/<str:param>", views_admin.view),
    path("admin/<str:param>/<str:record_id>", views_admin.view),
    path("login", views_login.view),
    path("report/<str:name>", views_report.view),
    path("transactions", views_transaction.view),
    path("transactions/<int:num>", views_transaction.view),
    path("doc/banstat", views_banstat2.view),
    path("doc/banstat/<str:acc>", views_banstat2.view),
    path("doc/<str:doc_type>", views_document.view),
    #path("doc/inv2/<str:num>", views_inv2.view),
    path("doc/eft/<str:num>", views_eft.view),
    path("doc/<str:doc_type>/<str:doc_num>", views_document.view),
]
