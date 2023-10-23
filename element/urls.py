from django.urls import path
from element import views


urlpatterns = [
    path("microorganisms/", views.microorganism_list),
    path("substrates/", views.substrate_list),
    path("products/", views.product_list),
]
