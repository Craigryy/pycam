from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),  # Root URL for the login page
    path('home/', views.homepage, name='home'),  # URL for the homepage
]
