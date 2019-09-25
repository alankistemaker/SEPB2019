from django.urls import path
from . import views




urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change_pw/', views.change_password, name='Change_pw'),

]