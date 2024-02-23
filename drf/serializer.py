from rest_framework import serializers
from inventory.models import Product , ProductInventory, Brand , ProductAttributeValue , Media , Category



class MediaSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta : 
        model = Media
        fields = ["image" , "alt_text" , ]

  
    def get_image(self,obj):
    #    return self.context["request"].build_absolute_uri(obj.image.url)
        return obj.image.url

class ProductAttributeValueSerializer(serializers.ModelSerializer):

    class Meta: 
        model = ProductAttributeValue
        exclude = ["id"]
        depth = 2
  

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name" , "slug", "is_acitve"]

class BrandSerializer (serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]
        read_only = True

class ProductSerializer (serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["name" , "web_id" ,"slug" , "description" , "category", "is_active"]







class ProductInventorySerializer(serializers.ModelSerializer):

    brand = BrandSerializer(many=False ,read_only = True )
    attributes = ProductAttributeValueSerializer(source = "attribute_values",many=True)
    image= MediaSerializer(source="media_product_inventory", many=True)
    product = ProductSerializer(many=False , read_only=True)
    class Meta : 
        model = ProductInventory
        fields = [
                 'id',
                 "sku",
                 "store_price" , 
                 "is_default" ,
                 "image",
                 "product",
                 "product_type" ,
                 "brand" ,
                  "attribute"
            
                 
                 ]
        


class ProductInventorySearchSerializer(serializers.ModelSerializer):

    product = ProductSerializer(many=False, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)

    class Meta:
        model = ProductInventory
        fields = [
            "id",
            "sku",
            "store_price",
            "is_default",
            "product",
            "brand",
        ]