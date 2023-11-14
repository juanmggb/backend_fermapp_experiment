from django.urls import path
from analysis.simulation.views import simulation

urlpatterns = [
    path("simulation/", simulation),
]
