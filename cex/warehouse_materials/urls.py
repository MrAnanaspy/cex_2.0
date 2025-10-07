from django.urls import path
from . import views

urlpatterns = [
    path('', views.warehouse_material, name='warehouse_material'),
    path('add_material/', views.add_material, name='add_material'),
    path('add_stamp/', views.add_stamp, name='add_stamp'),
    path('edit_stamp/<str:stamp>', views.edit_stamp, name='edit_stamp'),

]