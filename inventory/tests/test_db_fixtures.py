from django.db import IntegrityError
import pytest
from inventory import models
import factories
# import models


@pytest.mark.dbfixture
@pytest.mark.parametrize("id , name, slug, is_active ",
                         [
                             (1, "fashion", "fashion", 1),
                             (2, "woman", "woman", 1),])
#                             (35, "baseball", "baseball", 1),])
def test_inventory_category_dbfixture(db, django_fixture_setup, id, name, slug, is_active):

    result = models.Category.objects.get(id=id)
    assert result.name == name
    assert result.slug == slug
    assert result.is_active == is_active


@pytest.mark.parametrize("slug, is_active",
                         [
                             ("django", 1),
                             ("django-models", 1),
                             ("baseball", 1),])
def test_inventory_db_category_insert_data(db,  slug, is_active):
    result = factories.CategoryFactory(slug=slug, is_active=is_active)
   # assert result.name == name
    assert result.slug == slug
    assert result.is_active == is_active


@pytest.mark.dbfixture
@pytest.mark.parametrize("id , web_id, name , slug , description, is_active, created_at, updated_at",
                         [
                             (
                                 1,
                                 "45425810",
                                 "widstar running sneakers",
                                 "widstar-running-sneakers",
                                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin porta, eros vel sollicitudin lacinia, quam metus gravida elit, a elementum nisl neque sit amet orci. Nulla id lorem ac nunc cursus consequat vitae ut orci. In a velit eu justo eleifend tincidunt vel eu turpis. Praesent eu orci egestas, lobortis magna egestas, tincidunt augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vitae lectus eget tortor laoreet efficitur vel et leo. Maecenas volutpat eget ante id tempor. Etiam posuere ex urna, at aliquet risus tempor eu. Aenean a odio odio. Nunc consectetur lorem ante, interdum ultrices elit consectetur sit amet. Vestibulum rutrum interdum nulla. Cras vel mi a enim eleifend blandit. Curabitur ex dui, rutrum et odio sit amet, auctor euismod massa.",
                                 1,
                                 "2022-01-01 14:18:33",
                                 "2022-01-01 14:18:33",
                             ),
                             (
                                 8616,
                                 "45434425",
                                 "impact puse dance shoe",
                                 "impact-puse-dance-shoe",
                                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin porta, eros vel sollicitudin lacinia, quam metus gravida elit, a elementum nisl neque sit amet orci. Nulla id lorem ac nunc cursus consequat vitae ut orci. In a velit eu justo eleifend tincidunt vel eu turpis. Praesent eu orci egestas, lobortis magna egestas, tincidunt augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vitae lectus eget tortor laoreet efficitur vel et leo. Maecenas volutpat eget ante id tempor. Etiam posuere ex urna, at aliquet risus tempor eu. Aenean a odio odio. Nunc consectetur lorem ante, interdum ultrices elit consectetur sit amet. Vestibulum rutrum interdum nulla. Cras vel mi a enim eleifend blandit. Curabitur ex dui, rutrum et odio sit amet, auctor euismod massa.",
                                 1,
                                 "2022-01-01 14:18:33",
                                 "2022-01-01 14:18:33",

                             )

                         ])
def test_inventory_db_product_dbfixture(db, django_fixture_setup,  id, web_id, name, slug, description, is_active, created_at, updated_at):

    result = models.Product.objects.get(id=id)
    result_created_at = result.created_at.strftime("%Y-%m-%d %H:%M:%S")
    result_updated_at = result.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    assert result.web_id == web_id
    assert result.name == name
    assert result.slug == slug
    assert result.description == description
    assert result.is_active == is_active
    assert result_created_at == created_at
    assert result_updated_at == updated_at


def test_inventory_db_product_uniqueness_intergrity(db):
    new_web_id = factories.ProductFactory.create(web_id=1234567890)
    with pytest.raises(IntegrityError):
        factories.ProductFactory.create(web_id=1234567890)


@pytest.mark.dbfixture
def test_inventory_db_product_insert_data(db):
    new_category = factories.CategoryFactory.create()
    new_product = factories.ProductFactory.create(
        category=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

    retult_product_category = new_product.category.all()

    print(retult_product_category)
    retult_product_category = new_product.category.all().count()

    assert "web_id_" in new_product.web_id
    assert retult_product_category == 10
