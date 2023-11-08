from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/', include('restaurants.urls')),
    path('api/', include('categories.urls')),
    path('api/', include('items.urls')),
    path('api/', include('menus.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
