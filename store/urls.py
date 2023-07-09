from django.urls import path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register("products", views.ProductViewSet, basename="products")
product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

router.register("collections", views.CollectionViewSet)
router.register("carts", views.CartViewSet)

urlpatterns = router.urls + product_router.urls
