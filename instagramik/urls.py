"""
Instagramik URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static
from instagramik import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # Второй вариант, более новый и "простой"
    path('', include('core.urls')),
    # Аналогичен записи:
    # url(r'', include('core.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

