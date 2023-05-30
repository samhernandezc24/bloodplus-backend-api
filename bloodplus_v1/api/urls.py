from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('', views.getRoutes, name='get_routes'),
    path('usuarios/', views.UserRegistrationView, name='user_registration'),
    path('usuarios/lista/', views.UserListView, name='user_list'),
    path('usuarios/me/', views.CurrentUserView, name='current_user'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
