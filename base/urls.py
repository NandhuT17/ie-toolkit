from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/',views.login_page,name="login"),
    path('register-user',views.register_user,name="register_user"),
    path('logout',views.logout_user,name="logout_user"),
    path('operators/', views.operators, name='operators'),
    path('machines/', views.machines, name='machines'),
    path('time-study/', views.time_study, name='time_study'),
    path('history/', views.history, name='history'),   
    path('export/', views.export_excel, name='export_excel'),
    path('get-operator/', views.get_operator, name='get_operator'),
]