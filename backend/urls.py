from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import MyTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    # Experiments
    path("", include("experiment.urls")),
    path("", include("element.urls")),
    # Analysis
    path("", include("analysis.simulation.urls")),
    path("", include("analysis.optimization.urls")),
    # login
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
