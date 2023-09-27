from django.urls import path 
from rest_framework.routers import DefaultRouter

from analysis import views

router = DefaultRouter()
router.register(r"analyses", views.AnalysisViewSet)

urlpatterns = router.urls