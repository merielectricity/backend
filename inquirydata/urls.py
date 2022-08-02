#urls.py (app)
from django.urls import path
from . import views

urlpatterns = [
    path('inquiry/', views.addData),
    path('', views.getData),
]
