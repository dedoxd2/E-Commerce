from django.shortcuts import render
from inventory import models


def home(requrest):

    return render(requrest, "index.html")


def category(request):
    data = models.Category.objects.all()
    print(models.Category.objects.all().query)
    return render(request, "categories.html", {"data": data})


def product_by_category(request, category):

    print(category)
    data = models.Product.objects.filter(category__name=category).values(
        "id", "name", "slug", "category__name", "product__store_price")

    return render(request, "product_by_category.html", {"data": data})


def product_details(request, id):
    from django.contrib.postgres.aggregates import ArrayAgg
    from django.db.models import Count
    filter_arguments = []

    if request.GET:
        for value in request.GET.values():
            filter_arguments.append(value)

        data = models.ProductInventory.objects.filter(  # Dynamic Filter using GET Parameters
            product__id=id).filter(
            attribute_values__attribute_value__in=filter_arguments).annotate(
            num_tags=Count("attribute_values")).filter(
            num_tags=len(filter_arguments)).values("id", "product__name", "sku", "store_price", "product_inventory__units", "product__slug").annotate(field_a=ArrayAgg("attribute_values__attribute_value")).get()

    else:

        data = models.ProductInventory.objects.filter(
            product__id=id).filter(is_default=True).values(
                "id", "product__name", "sku", "store_price",
                "product_inventory__units", "product__slug"
        ).annotate(field_a=ArrayAgg("attribute_values__attribute_value")).get()

    slug = data["product__slug"]

    y = models.ProductInventory.objects.filter(product__slug=slug).distinct().values(
        "attribute_values__product_attribute__name", "attribute_values__attribute_value")

    print(y)

    z = models.ProductTypeAttribute.objects.filter(
        product_type__product_type__product__slug=slug).values("product_attribute__name").distinct()
    print(z)

    return render(request, "product_details.html", {"data": data, "y": y, "z": z})
