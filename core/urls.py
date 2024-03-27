from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('auth_app.urls')),
                  path('', include('dashboard_app.urls')),
                  path('', include('hr_app.urls')),
                  path('', include('inventory_app.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
