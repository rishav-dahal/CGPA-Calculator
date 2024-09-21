from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-subject-grade/<int:semester_id>/', views.add_subject_grade, name='add_subject_grade'),


    # Test URLs
    path('calculate-sgpa/<int:semester_id>/', views.calculate_sgpa_view, name='calculate_sgpa'),
    path('calculate-cgpa/<int:user_id>/', views.calculate_cgpa_view, name='calculate_cgpa'),
    
]
