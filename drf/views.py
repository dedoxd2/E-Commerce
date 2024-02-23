from inventory.models import Product, ProductInventory
from rest_framework import  permissions , generics  , status
from rest_framework.views import APIView  
from rest_framework.response import Response
from .serializer import ProductSerializer , ProductInventorySerializer
from rest_framework.pagination import  LimitOffsetPagination
from django.core.exceptions import ObjectDoesNotExist


def check_product_Existence(slug=None):
    product = Product.objects.filter(slug=slug).first()
    if product :
        return product
    else:
        raise ObjectDoesNotExist
class AllProductsViewset(generics.ListCreateAPIView , generics.RetrieveUpdateDestroyAPIView):
    """
    GET -> Get All products Paginated
    POST -> Create new Product
    Put -> update all Product data
    patch -> partially update product
    """

    queryset = Product.objects.all()  
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
     
    def post (self, request,slug=None):
        newProduct = ProductSerializer(data= request.data)
        if newProduct.is_valid():
            newProduct.save()
            return Response(newProduct.data , status= status.HTTP_201_CREATED)
        else: 
            return Response(newProduct.errors,status=status.HTTP_400_BAD_REQUEST)

   
    def put(self,request,slug=None):
        
        product = check_product_Existence(slug=slug)
        newProduct = ProductSerializer(product,data=request.data)
        if newProduct.is_valid():
            newProduct.save()
            return Response(newProduct.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response(newProduct.errors,status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request,slug=None):
        product = check_product_Existence(slug=slug)

        newProduct = ProductSerializer(product,data=request.data,partial=True)
        if newProduct.is_valid():
            newProduct.save()
            return Response(newProduct.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response(newProduct.errors,status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request,slug= None):
             

        product = check_product_Existence(slug=slug)

        product.delete()
        return Response ("product deleted",status=status.HTTP_204_NO_CONTENT)



class ProductInventoryViewset(APIView):

 #   queryset = ProductInventory.objects.all()
   # serializer_class = ProductInventorySerializer

    def get(self, request , slug = None):


        queryset = ProductInventory.objects.filter(product__category__slug=slug).filter(is_default= True)[:10]
        serializer = ProductInventorySerializer(queryset,context = {"request":request} , many=True)

        return Response(serializer.data)

        