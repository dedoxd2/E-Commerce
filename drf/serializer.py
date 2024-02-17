from rest_framework import serializers
from inventory.models import Product , ProductInventory, Brand , ProductAttributeValue , Media



class MediaSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta : 
        model = Media
        fields = ["image" , "alt_text" , ]
        read_only = True
  
  
    def get_image(self,obj):
        return self.context["request"].build_absolute_uri(obj.image.url)

class ProductAttributeValueSerializer(serializers.ModelSerializer):

    class Meta: 
        model = ProductAttributeValue
        exclude = ["id"]
        depth = 2

class BrandSerializer (serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]

class AllProducts (serializers.ModelSerializer):
    """
    Product Serializer
    """
    class Meta:
        model = Product
        fields = ["name"]
       # exclude = ["name"]
        read_only = True
        editale = False
        #depth = 2





class ProductInventorySerializer(serializers.ModelSerializer):

    # brand = BrandSerializer(many=False ,read_only = True )
    # attribute = ProductAttributeValueSerializer(source = "attribute_values",many=True)
    # image= MediaSerializer(source="media_product_inventory", many=True)

    product = AllProducts(many=False , read_only=True)
    class Meta : 
        model = ProductInventory
        fields = [
                # 'id',
                # "sku",
                # "store_price" , 
                # "is_default" ,
                # "image",
                # "product",
                # "product_type" ,
                # "brand" ,
                #  "attribute"
            'id',
            "sku",
            'store_price' , 
            "is_default",
            "product"
                 
                 ]
        
        read_only = True
        #depth = 1