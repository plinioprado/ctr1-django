from django.urls import path
from . import views_reset
from . import views_num
from . import views

urlpatterns = [
    path('reset/', views_reset.invoice1),
    path('<int:num>/', views_num.invoice1),
    path('', views.invoice1)
]
