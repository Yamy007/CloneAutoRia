from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from config.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path("", include("core.swagger.swagger")),  # swagger
    path("api/", include("apps.users.urls")),
    path("api/", include("apps.advertisements.urls")),
    path("api/", include("apps.auth.urls")),  # auth login,refresh
]
urlpatterns += static(MEDIA_URL, document_root=settings.MEDIA_ROOT)
