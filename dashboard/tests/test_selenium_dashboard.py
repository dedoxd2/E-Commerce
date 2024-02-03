import pytest
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys


# pytestmark = pytest.mark.django_db
# @pytest.mark.selenium

# @pytest.mark.django_db
@pytest.mark.selenium
def test_dashboard_admin_login(live_server, django_fixture_setup, firefox_browser_instance):
    browser = firefox_browser_instance
    browser.get(("%s%s" % (live_server.url, "/admin/login/")))

    user_name = browser.find_element(By.NAME, "username")
    user_password = browser.find_element(By.NAME, "password")
    submit = browser.find_element(By.XPATH, '//input[@value="Log in"]')

    user_name.send_keys("admin")
    user_password.send_keys("password")
    submit.send_keys(Keys.RETURN)

    assert "Django administration" in browser.page_source
