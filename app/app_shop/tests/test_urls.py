import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from app.app_shop.models.products import Product, CategoryProduct


class TestUrls(TestCase):
    """
    Проверка доступности страниц по URL-адресам
    """

    @classmethod
    def setUpTestData(cls):
        """
        Метод создает тестовых пользователя и категорию перед тестированием
        """

        test_user = User.objects.create(
            username="test_user", password="secret_password"
        )
        test_img = open(os.path.join("app_shop", "tests", "test_img.jpg"), "rb").read()

        test_category = CategoryProduct.objects.create(
            title="Тестовая категория",
            image=SimpleUploadedFile(
                name="test_img.jpg", content=test_img, content_type="image/jpeg"
            ),
        )

        # test_tag = ProductTags.objects.create(name='Тестовый тег')
        test_post = Product.objects.create(
            name="Тестовый товар",
            definition="Описание тестового товара",
            characteristics={},
            category=test_category,
            # tags=test_tag,
            price=100,
        )

    def test_main(self):
        """
        Проверка доступности главной страницы
        """
        resource = self.client.get(reverse("shop:main"))
        self.assertEqual(resource.status_code, 200)
