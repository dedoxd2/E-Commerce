from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import pytest
from django.contrib.auth.models import User
from django.core.management import call_command


@pytest.fixture
def create_admin_user(django_user_model):
    """
    Return Admin User
    """
    return django_user_model.objects.create_superuser("admin", "a@a.com", "password")


@pytest.fixture(scope="function")
def firefox_browser_instance(request):
    """
     Provide a selenium webdriver instance
    """
    options = Options()
    options.headless = False
    browser = webdriver.Firefox(options=options)
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def django_fixture_setup(django_db_setup, django_db_blocker):
    """
    Load DB data fixtures
    """
    with django_db_blocker.unblock():
        call_command("loaddata", "db_admin_fixture.json")
        call_command("loaddata", "db_category_fixture.json")
        call_command("loaddata", "db_product_fixture.json")
