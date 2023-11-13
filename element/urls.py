from django.urls import path
from element import views


urlpatterns = [
    # Microorganism
    path("microorganisms/", views.microorganism_list),
    path("microorganisms/<int:id>/", views.microorganism_details),
    # Substrates
    path("substrates/", views.substrate_list),
    path("substrates/<int:id>/", views.substrate_details),
    # Products
    path("products/", views.product_list),
    path("products/<int:id>/", views.product_details),
]
