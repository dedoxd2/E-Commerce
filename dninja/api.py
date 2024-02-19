from typing import List
from ninja import NinjaAPI
from .schema import CategorySchema , ProductSchema , InvebtorySchema
from inventory.models import Category, Product, ProductInventory

api = NinjaAPI()


@api.get("/inventory/category/all/" , response = List[CategorySchema])
def categroy_list(request):
    qs = Category.objects.filter(is_active=True)
    return qs



@api.get("/inventory/product/category/{category_slug}/" ,response=List[ProductSchema])
def categroy_retrieve (request , category_slug: str):
    qs = Product.objects.filter(category__slug = category_slug)
    return qs


@api.get("/inventory/{web_id}/" , response=List[InvebtorySchema])
def inventory_list(request, web_id:str ):
    qs = ProductInventory.objects.filter(product__web_id = web_id)
    return qs 