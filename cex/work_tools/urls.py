from django.urls import path
from . import views

urlpatterns = [
    path('tool/info/<int:id>/', views.info_tool, name='info_tool'),
    path('tool/add/<str:type>/', views.add_tool, name='add_tool'),
    path('tools/parse/', views.parse_tool, name='parse_tool'),
    path('tools/', views.tools, name='tools'),
]