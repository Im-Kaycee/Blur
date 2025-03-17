from django.contrib import admin
from django.urls import path, include
from users.views import profile_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('chat.urls')),
    path('profile/', include('users.urls')),
    path('@<username>/', profile_view, name="profile"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)