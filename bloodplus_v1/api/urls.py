from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'bloodplus_v1'

urlpatterns = [
    path('', views.getRoutes, name='get_routes'),
    path('usuarios/', views.user_list_view, name='user_list'),
    path('usuarios/<int:pk>', views.user_detail_view, name='user_detail'),
    path('usuarios/crear/', views.user_create_view, name='user_create'),
    path('usuarios/me/', views.CurrentUserView, name='current_user'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
