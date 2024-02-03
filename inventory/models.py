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
