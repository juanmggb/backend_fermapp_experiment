from django.urls import path
from experiment import views


urlpatterns = [
    path("experiments/", views.experiment_list),
    path("experiments/<int:id>/", views.experiment_details),
]
