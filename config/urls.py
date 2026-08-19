from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/authcore/', include('apps.authcore.urls')),
    path('api/v1/messaging/', include('apps.messaging.urls')),
]
