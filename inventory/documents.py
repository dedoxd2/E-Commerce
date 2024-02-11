from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from inventory.models import ProductInventory


@registry.register_document
class ProductInventoryDocument(Document):
    # Every time you change a property in the index you have to use "python manage.py search_index --rebuild"

    product = fields.ObjectField(
        properties={
            "name": fields.TextField()
        }
    )

    product_inventory = fields.ObjectField(
        properties={
            "units": fields.IntegerField()
        }
    )

    class Index:
        name = "productinventory"

    class Django:
        model = ProductInventory
        fields = ["id", "sku"]


# Simple Query For  testing


# Using curl
# curl -X GET "localhost:9200/_search?pretty" -H 'Content-Type: application/json' -d'

# {
#     "query":{
#         "bool":{

#             "must":[

#                 {"match": {"sku" :"7633969397"}}
#             ]
#         }

#     }


# }'

# Post Man
# Add Header
#   Content-Type: application/json
# Specify the end point and port
#        http://localhost:9200/_search?pretty
# Specify the Method
#        GET

# In the Body

# {
#     "query":{
#         "bool":{

#             "must":[

#                 {"match": {"sku" :"7633969397"}}
#             ]
#         }

#     }


# }
