# from django.contrib.auth.models import User
# import pytest
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options


# @pytest.fixture(scope="function")
# def firefox_browser_instance(request):
#     """
#      Provide a selenium webdriver instance
#     """
#     options = Options()
#     options.headless = False
#     browser = webdriver.Firefox(options=options)
#     yield browser
#     browser.close()


# # @pytest.fixture
# # def create_admin_user(django_user_model):
# #     """
# #     Return Admin User
# #     """
# #     return django_user_model.objects.create_superuser("admin", "a@a.com", "password")
