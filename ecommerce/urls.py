from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf import views
from search.views import SearchProductInventory

router = routers.DefaultRouter()
router.register(

    r'api', views.AllProductsViewset, basename="allproducts"
)

router.register(

    r'product/(?P<slug>[^/.]+)', views.ProductInventoryViewset, basename="products"
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', include("demo.urls", namespace="demo")),
    #  path("drf/", include("drf.urls", namespace="drf")),
    path("", include(router.urls)),
        path("search/<str:query>/",SearchProductInventory.as_view() ),    
]
