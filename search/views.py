from django.http import HttpResponse
from rest_framework.views import APIView   
from rest_framework.pagination import LimitOffsetPagination
from drf.serializer import ProductInventorySerializer
from .documets import ProductInventoryDocument
from elasticsearch_dsl import Q





class SearchProductInventory(APIView , LimitOffsetPagination):

    productinventory_serializer = ProductInventorySerializer
    search_doccument = ProductInventoryDocument

    def get(self,request , query):

        try: 
            q = Q('multi_match' , query=query ,fields= ['product.name'] , fuzziness = 'auto') 

            search = self.search_doccument.search().query(q)
            respose = search.execute()
            results = self.paginate_queryset(respose,request , view=self)
            serializer = self.productinventory_serializer(results,many=True)
            return self.get_paginated_response(serializer.data)

        except Exception as e :
            return HttpResponse(e,status =500)
