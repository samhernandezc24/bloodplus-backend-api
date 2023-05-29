from django.contrib import admin
from django.urls import include, path

from bloodplus_v1.api.views.user_views import MyTokenObtainPairView, getRoutes

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', getRoutes),
    path('api/v1/usuarios/', include('bloodplus_v1.api.urls')),

    path('api/v1/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('admin/', admin.site.urls),
]

handleNotFoundError = 'utils.error_views.handleNotFoundError'
handleServerError = 'utils.error_views.handleServerError'
