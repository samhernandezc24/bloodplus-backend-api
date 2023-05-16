from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('me/', views.currentUser, name='current_user'),
    path('me/actualizar/', views.updateUser, name='update_user'),
]
