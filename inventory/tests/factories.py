import factory
import pytest
from faker import Faker
from pytest_factoryboy import register
from inventory import models


fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Sequence(lambda n: "cat_slug_%d" % n)
    slug = fake.lexify(text="cat_slug_??????")


class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Product

    web_id = factory.sequence(lambda n: "web_id_%d" % n)
    slug = fake.lexify(text="prod_slug_?????")
    name = fake.lexify(text="prod_name_?????")
    description = fake.text()
    is_active = True
    created_at = "2021-09-04 22:14:18.222"
    created_at = "2021-09-04 22:14:18.222"

    @factory.post_generation
    def category(self, create, extracted, **kwards):
        if not create or not extracted:
            return

        if extracted:
            for cat in extracted:
                self.category.add(cat)


register(CategoryFactory)

register(ProductFactory)
