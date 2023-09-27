from django.urls import path 
from experiment import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"experiments", views.ExperimentViewSet)
router.register(r"experiment-variables", views.ExperimentVariableViewSet)
router.register(r"experiment-variables-values", views.ExperimentVariableValueViewSet)


urlpatterns = [
    *router.urls, 
    path("create-experiment/", views.CreateExperimentObjects.as_view())

]


