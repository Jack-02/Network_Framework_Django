from django.urls import path
from . import views

app_name = 'ESG'

urlpatterns = [
    path('', views.esg_index, name='esg_index'),
    path('index/', views.esg_index, name='esg_index1'),
    path('about/', views.esg_about, name='esg_about'),
    path('list/',views.esg_list, name='esg_list'),
    path('list/<id>/',views.esg_content, name='esg_content'),
    path('changelog/', views.esg_changelog, name='esg_changelog'),
    path('contact/', views.esg_contact, name='esg_contact'),
    path('login/', views.esg_login, name='esg_logiin'),
    path('stat/', views.esg_stat, name='esg_stat'),
    path('register/', views.esg_register, name='esg_register'),
    path('logout/', views.esg_logout, name='esg_logout'),
]