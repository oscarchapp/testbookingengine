
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("pms.urls")),
    path('unicorn/', include("django_unicorn.urls")),
]
