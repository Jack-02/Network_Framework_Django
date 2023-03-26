from django.urls import path
from login import views
urlpatterns = [
    path('index/',views.index,name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

]