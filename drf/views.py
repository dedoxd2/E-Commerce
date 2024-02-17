from inventory.models import Product, ProductInventory
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from .serializer import AllProducts , ProductInventorySerializer


class AllProductsViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):

    queryset = Product.objects.all()  # filter(is_active=True)
    serializer_class = AllProducts
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        queryset = Product.objects.filter(category__slug=slug)[:10]
        serializer = AllProducts(queryset, many=True)
        return Response(serializer.data)


class ProductInventoryViewset(viewsets.GenericViewSet, mixins.ListModelMixin):

    queryset = ProductInventory.objects.all()
   # serializer_class = ProductInventorySerializer

    def list(self, request , slug = None):


        queryset = ProductInventory.objects.filter(product__category__slug=slug).filter(is_default= True)[:10]
        serializer = ProductInventorySerializer(queryset,context = {"request":request} , many=True)

        return Response(serializer.data)

        