from django.urls import path
from . import views

urlpatterns = [
    path('', views.feature, name='feature'),  # Root URL for the login page
    path('home/', views.homepage, name='home'),  # URL for the homepage
    path('login/',views.login,name='login'),
    path('upload/', views.upload_image, name='upload_image'),
    path('save-edited-image/', views.save_edited_image, name='save_edited_image'), 
    path('edit/<int:image_id>/', views.edit_image, name='edit_image'),
    path('image/<int:image_id>/', views.view_image, name='view_image'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),  
]
