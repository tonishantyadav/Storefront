from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from . import filters, models, serializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    def destroy(self, request, *args, **kwargs):
        if models.OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = models.Collection.objects.annotate(products_count=Count("products"))
    serializer_class = serializers.CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if models.Product.objects.filter(collection=kwargs["pk"]).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return models.Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):  
    # pre-load items and product data
    queryset = models.Cart.objects.prefetch_related("items__product").all()
    serializer_class = serializers.CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CartItemSerializer

    # pre-load product data
    def get_queryset(self):
        return models.CartItem.objects.filter(
            cart_id=self.kwargs.get("cart_pk")
        ).select_related("product")
