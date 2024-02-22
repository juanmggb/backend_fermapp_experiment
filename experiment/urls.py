from django.urls import path
from experiment import views


urlpatterns = [
    path("experiments/", views.experiment_list, name="experiment-list"),
    path("experiments/<int:id>/", views.experiment_details, name="experiment-details"),
]
