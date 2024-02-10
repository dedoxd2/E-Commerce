from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


class Category(MPTTModel):
    """
    Inventory Category table implemented using MPTT
    """
    name = models.CharField(max_length=110, null=False,
                            unique=False, blank=False, verbose_name=_("category name"), help_text=_("format: required , max-110"))

    slug = models.SlugField(max_length=150, null=False,
                            unique=False, blank=False, verbose_name=_("category safe URL"), help_text=_("format: required , letters , numbers, underscore, or hyphens"))

    is_active = models.BooleanField(default=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, related_name="children", null=True, blank=True,
                            unique=False, verbose_name=_("parent of category"), help_text=_("format: not required",))

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """
    Product Details Table
    """
    web_id = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name=_(
        "product website ID"), help_text=_("format: required , unique"))

    slug = models.SlugField(max_length=255, unique=False, null=False, blank=False, verbose_name=_(
        "product safe URL"), help_text=_("fromat: required, letters, numbers, underscored or hyphens"))

    name = models.CharField(max_length=255, unique=False, null=False, blank=False, verbose_name=_(
        "product name"), help_text=_("format: requiredm max length 255"))

    description = models.TextField(unique=False, null=False, blank=False, verbose_name=_(
        "product: description"), help_text=_("format: required"),)

    category = TreeManyToManyField(Category)

    is_active = models.BooleanField(unique=False, null=False, blank=False, default=True, verbose_name=_(
        "product visibility"), help_text=_("format: true = product will be visible"))

    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_(
        "date product created"), help_text=_("fromat: Y-M-D H:M:S"),)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_(
        "date product last updated"), help_text=_("fromat: Y-M-D H:M:S"),)

    def __str__(self):
        return self.name


class Brand(models.Model):
    """
    Product brand table
    """
    name = models.CharField(
        max_length=255,
        unique=True, null=False, blank=False, verbose_name=_("brand name"), help_text=_("format: required, max-255"))

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False,
                            blank=False, verbose_name=_("Product attribute name"), help_text=_("format: required , unique , max-255"))

    description = models.TextField(unique=False, null=False, blank=False, verbose_name=_(
        "product attribute description"), help_text=_("format: required"))

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    """
    Product Attribute Value Table
    """

    attribute_value = models.CharField(max_length=255, unique=False,  blank=False, null=False, verbose_name=_(
        "value for attribute of product"), help_text=_("format: text or numbers , required , maxlength = 255 ,  ,unique = False,  blank = False, null= False"))

    product_attribute = models.ForeignKey(
        ProductAttribute, related_name="product_attribute", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.product_attribute.name} : {self.attribute_value}"


class ProductType (models.Model):
    """
    Product type table
    """

    name = models.CharField(max_length=255, unique=True, null=False, blank=False, verbose_name=_(
        "type of product"), help_text=_("format: required, unique, max-255",))

    product_type_attributes = models.ManyToManyField(
        ProductAttribute, related_name="product_type_attributes", through="ProductTypeAttribute")

    def __str__(self):
        return self.name


class ProductTypeAttribute(models.Model):
    """
    Product type attributes link table
    """

    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="productattribute",
        on_delete=models.PROTECT,
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name="producttype",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = (("product_attribute", "product_type"),)


class ProductInventory(models.Model):
    """
    Product inventory table
    """
    sku = models.CharField(max_length=20, unique=True, null=False, blank=False, verbose_name=_(
        "stock keeping unit"), help_text=_("format: required , unique, max-20"))

    upc = models.CharField(max_length=12, unique=True, null=False, blank=False, verbose_name=_(
        "universal product code"), help_text=_("format: required, unique, max-12"))

    product_type = models.ForeignKey(
        ProductType, related_name="product_type", on_delete=models.PROTECT)
    product = models.ForeignKey(
        Product, related_name="product", on_delete=models.PROTECT)
    brand = models.ForeignKey(
        Brand, related_name="brand", on_delete=models.PROTECT)

    attribute_values = models.ManyToManyField(
        ProductAttributeValue, related_name="product_attribute_values", through="ProductAttributeValues",)

    is_active = models.BooleanField(default=True, verbose_name=_(
        "default selection"), help_text=_("format: true = sub product visible"))

    is_default = models.BooleanField(default=False, verbose_name=_(
        "product visibility"), help_text=_("format: true = product visible"))

    retail_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        blank=False,
        null=False,
        verbose_name=_("recommended retail price"),
        help_text=_("format: maximum price 999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99")
            }
        }
    )
    store_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        blank=False,
        null=False,
        verbose_name=_("regular store price"),
        help_text=_("format: maximum price 999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99")
            }
        }
    )

    sale_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        blank=False,
        null=False,
        verbose_name=_("sale price"),
        help_text=_("format: maximum price 999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99")
            }
        }
    )

    weight = models.FloatField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("product weight"),
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("date sub-product created"),
                                      help_text=_("format: Y-m-d H:M:S"),
                                      )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("date sub-product updated"),
                                      help_text=_("format: Y-m-d H:M:S"),
                                      )

    def __str__(self):
        return self.product.name


class Media(models.Model):
    """
    Product Image Table
    """

    product_inventory = models.ForeignKey(
        ProductInventory, on_delete=models.PROTECT, related_name="media_product_inventory", )

    image = models.ImageField(unique=False, null=False, blank=False, verbose_name=_(
        "Product Image"), upload_to="images/", default="images/default.png", help_text=_("format: required, default value - default.png"))

    alt_text = models.CharField(max_length=255, unique=False, null=False, blank=False, verbose_name=_(
        "alternative text"), help_text=_("format: required , max-255"))

    is_feature = models.BooleanField(
        default=False, verbose_name=_("product default image"), help_text=_("format: (default value = false) , (true= this image will be the default image for the product) "))

    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("date sub-product created"),
                                      help_text=_("format: Y-m-d H:M:S"),
                                      )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("date sub-product updated"),
                                      help_text=_("format: Y-m-d H:M:S"),
                                      )

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")


class Stock(models.Model):
    product_inventory = models.OneToOneField(
        ProductInventory, related_name="product_inventory", on_delete=models.PROTECT)

    last_checked = models.DateTimeField(unique=False, null=True, blank=True, verbose_name=_(
        "inventory stock check date"), help_text=_("format: Y-m-d H:M:S, null = True , blank = True"))

    units = models.IntegerField(default=0, unique=False, null=False, blank=False, verbose_name=_(
        "units/qty of stock"), help_text=_("format: required, default = 0"))
    units_sold = models.IntegerField(default=0, unique=False, null=False, blank=False, verbose_name=_(
        "units sold till current date"), help_text=_("format: required, default = 0"))


class ProductAttributeValues(models.Model):
    """
    Product Attribute values Link Table
    """
    attribute_values = models.ForeignKey(
        ProductAttributeValue, related_name="attribute_values", on_delete=models.PROTECT)

    product_inventory = models.ForeignKey(
        ProductInventory, related_name="product_attribute_values", on_delete=models.PROTECT)

    class Meta:
        unique_together = (("attribute_values", "product_inventory"))
