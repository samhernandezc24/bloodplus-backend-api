from django.urls import path
from .views import user_views

urlpatterns = [
    path('', user_views.register, name='register'),
    path('me/', user_views.currentUser, name='current_user'),
]
