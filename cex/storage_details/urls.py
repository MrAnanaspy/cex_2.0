from django.urls import path
from . import views

urlpatterns = [
    path('create_specification/', views.create_specification, name='create_specification'),
]