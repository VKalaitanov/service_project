from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('secure-admin-path/', admin.site.urls),
    path('', include('service.urls', namespace='service')),
    path('users/', include('users.urls', namespace='users')),
    path('order/', include('orders.urls', namespace='order')),
    path("chat/", include("chat.urls")),
    # path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
