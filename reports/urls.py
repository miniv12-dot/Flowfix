from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # <-- The new home page route
    path('report/', views.report_fault, name='report_fault'),
    path('map/', views.public_map, name='public_map'),
    path('dashboard/', views.municipality_dashboard, name='dashboard'),
    path('track/', views.track_report, name='track_report'),
]