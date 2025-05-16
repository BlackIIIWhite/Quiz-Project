"""
URL configuration for quiz_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('login/', views.LoginPage, name='login'),
    path('signup/', views.SignupPage, name='signup'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz_an/', views.quiz_an, name='quiz_an'),
    path('dashboard_st/', views.dashboard_st, name='dashboard_st'),
    path('dashboard_student/', views.dashboard_student, name='dashboard_student'),
    path('result/', views.result, name='result'),
    path('quiz_create/', views.quiz_create, name='quiz_create'),
    path('test_info/', views.test_info, name='test_info'),
    path('create_class/', views.create_class, name="create_class"),
    path('join_class/', views.join_class, name='join_class'),
    path('join_test/', views.join_test, name='join_test'),
    path('upload_test/', views.upload, name="upload"),
    path('file_upload/', views.file, name="file"),
    path('result_student/', views.result_student, name='result_student'),
    path('login_teach/', views.LoginPage_teacher, name='login_teach'),
    path('signup_teach/', views.SignupPage_teacher, name='signup_teach'),
    path('logout/', views.LogoutPage, name='logout'),
    path('logout_teach/', views.LogoutPage_teacher, name='logout_teach'),
]
