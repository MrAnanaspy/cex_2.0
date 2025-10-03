from django.urls import path
from . import views

urlpatterns = [
    path('', views.warehouse_material, name='warehouse_material'),
]