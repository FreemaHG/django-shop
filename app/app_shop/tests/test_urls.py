from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestUrls(TestCase):
    """
    Проверка доступности url, связанных с магазином (главная страница, страница товара, оформления заказа и т.п.)
    """

    # fixtures = ['app/fixtures/test-data.json']

    def test_main_url(self):
        """
        Проверка доступности главной страницы по url
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_main_url_name(self):
        """
        Проверка доступности главной страницы по url-name
        """
        response = self.client.get(reverse("shop:main"))
        self.assertEqual(response.status_code, 200)

    def test_about_url(self):
        """
        Проверка доступности страницы о магазине по url
        """
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)

    def test_about_url_name(self):
        """
        Проверка доступности страницы о магазине по url-name
        """
        response = self.client.get(reverse("shop:about"))
        self.assertEqual(response.status_code, 200)

    def test_sale_url(self):
        """
        Проверка доступности страницы с распродажей по url
        """
        response = self.client.get("/sale/")
        self.assertEqual(response.status_code, 200)

    def test_sale_url_name(self):
        """
        Проверка доступности страницы с распродажей по url-name
        """
        response = self.client.get(reverse("shop:sale"))
        self.assertEqual(response.status_code, 200)

    def test_catalog_url(self):
        """
        Проверка доступности страницы с каталогом товаров по url
        """
        response = self.client.get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_url_name(self):
        """
        Проверка доступности страницы с каталогом товаров по url-name
        """
        response = self.client.get(reverse("shop:products_list"))
        self.assertEqual(response.status_code, 200)

    def test_search_url(self):
        """
        Проверка доступности страницы поиска товаров по url
        """
        response = self.client.get("/search/", data={"query": ""})
        self.assertEqual(response.status_code, 200)

    def test_search_url_name(self):
        """
        Проверка доступности страницы поиска товаров по url-name
        """
        response = self.client.get(reverse("shop:search"), data={"query": ""})
        self.assertEqual(response.status_code, 200)
