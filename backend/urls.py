from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/", include("users.urls")),
    # Experiments
    path("api/", include("experiment.urls")),
    path("api/", include("element.urls")),
    # # Analysis
    path("api/", include("analysis.simulation.urls")),
    path("api/", include("analysis.optimization.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
