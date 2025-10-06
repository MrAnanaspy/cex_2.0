from django.urls import path
from . import views

urlpatterns = [
    path('', views.warehouse_material, name='warehouse_material'),
    path('add_material/', views.add_material, name='add_material'),

]