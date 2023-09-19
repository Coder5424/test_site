from django.urls import path
from . import views

urlpatterns = [
    path('init_db/', views.init_db, name='init_db'),
    path('', views.studies_view, name='studies')
]