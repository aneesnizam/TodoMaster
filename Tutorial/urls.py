
from django.contrib import admin
from django.urls import path
from MyApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('home/', views.home, name="home"),
    path('', views.landing, name="landing"),
    path('demo/', views.demo, name="demo"),
    path('how-it-works/', views.howItWorks, name="howItWorks"),
    path('features/', views.features, name="features"),
    path('logout/', views.logout, name="logout"),
    path('add-task/', views.addTask, name="addTask"),
    path('profile/', views.profile, name="profile"),
    path('important/', views.important, name="important"),
    path('today/', views.today, name="today"),
    path('completed/', views.completed, name="completed"),
    path('adminPanel/', views.adminPanel, name="adminPanel"),
    path('adminLogin/', views.adminLogin, name="adminLogin"),
    path('adminTable/', views.adminTable, name="adminTable"),
    path('adminApproval/', views.adminApproval, name="adminApproval"),
    path('approve/<int:userId>/', views.approve_user, name="approve_user"),
    path('revoke/<int:userId>/', views.revoke_user, name="revoke_user")

]
