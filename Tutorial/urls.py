
from django.contrib import admin
from django.urls import path
from MyApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_user, name="login"),
    path('register/', views.register, name="register"),
    path('home/', views.home, name="home"),
    path('', views.landing, name="landing"),
    path('demo/', views.demo, name="demo"),
    path('how-it-works/', views.howItWorks, name="howItWorks"),
    path('features/', views.features, name="features"),
    path('logout/', views.logoutUser, name="logout"),
    path('add-task/', views.addTask, name="addTask"),
    path('profile/', views.profile, name="profile"),
    path('important/', views.important, name="important"),
    path('today/', views.today, name="today"),
    path('completed/', views.completed, name="completed"),
    path('adminPanel/', views.adminPanel, name="adminPanel"),
    path('adminLogin/', views.adminLogin, name="adminLogin"),

    path('adminApproval/', views.adminApproval, name="adminApproval"),
    path('approve/<int:userId>/', views.approve_user, name="approve_user"),
    path('revoke/<int:userId>/', views.revoke_user, name="revoke_user"),
    path('mark_as_complete/<int:taskid>',
         views.mark_as_complete, name="mark_as_complete"),
    path('important_toggle/<int:taskid>',
         views.important_toggle, name="important_toggle"),
    path('delete_item/<int:taskid>',
         views.delete_item, name="delete_item"),
        path('delete_user/<int:taskid>',
         views.delete_user, name="delete_user"),
        path('admin_logout/', views.admin_logout, name="admin_logout"),
            path('create-admin/', views.create_admin),


]
