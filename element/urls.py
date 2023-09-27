from element import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"substrates", views.SubstrateViewSet)
router.register(r"microorganisms", views.MicroorganismViewSet)
router.register(r"products", views.ProductViewSet)

urlpatterns = router.urls