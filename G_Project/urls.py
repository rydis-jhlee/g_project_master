from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('user.urls')),
    path('', include('sale.urls')),
    path('', include('payments.urls')),
    path('', include('delivery.urls')),
    path('', include('webapp.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)