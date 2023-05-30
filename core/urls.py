from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('bloodplus_v1.api.urls')),
]

handleNotFoundError = 'utils.error_views.handleNotFoundError'
handleServerError = 'utils.error_views.handleServerError'
