from django.contrib import admin
from .models import Category, Product , ProductAttribute , ProductAttributeValue, ProductAttributeValues, ProductType, ProductTypeAttribute ,Media 
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(ProductType)
admin.site.register(ProductTypeAttribute)
admin.site.register(ProductAttributeValues)
admin.site.register(Media)