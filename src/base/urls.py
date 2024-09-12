from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),


    # Test URLs
    path('calculate-sgpa/<int:semester_id>/', views.calculate_sgpa_view, name='calculate_sgpa'),
    path('calculate-cgpa/<int:user_id>/', views.calculate_cgpa_view, name='calculate_cgpa'),
    
]
