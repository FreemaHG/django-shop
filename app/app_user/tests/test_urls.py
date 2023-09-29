from django.test import TestCase
from django.urls import reverse


class TestUrls(TestCase):
    """
    Проверка доступности url, связанных с пользователем (авторизация, личный кабинет и т.п.)
    """

    def test_register_url(self):
        """
        Проверка доступности страницы регистрации по url
        """
        response = self.client.get("/my/registration/")
        self.assertEqual(response.status_code, 200)

    def test_register_url_name(self):
        """
        Проверка доступности страницы регистрации по url-name
        """
        response = self.client.get(reverse("user:registration"))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        """
        Проверка доступности страницы авторизации по url
        """
        response = self.client.get("/my/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_url_name(self):
        """
        Проверка доступности страницы авторизации по url-name
        """
        response = self.client.get(reverse("user:login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        """
        Проверка доступности страницы выхода по url
        """
        # Авторизуем тестового пользователя
        self.client.login(username="test_user", password="secret_password")
        # Запрос от авторизованного пользователя
        response = self.client.get("/my/logout/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logout_url_name(self):
        """
        Проверка доступности страницы выхода по url-name
        """
        # Запрос от авторизованного пользователя
        response = self.client.get(reverse("user:logout"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_password_recovery_url(self):
        """
        Проверка доступности страницы смены пароля по url
        """
        # Запрос от авторизованного пользователя
        response = self.client.get("/my/password_recovery/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_password_recovery_url_name(self):
        """
        Проверка доступности страницы смены пароля по url-name
        """
        # Запрос от авторизованного пользователя
        response = self.client.get(reverse("user:password_recovery"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_account_url(self):
        """
        Проверка доступности страницы личного кабинета по url
        """
        # Запрос от авторизованного пользователя
        response = self.client.get("/my/account/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_account_name(self):
        """
        Проверка доступности страницы личного кабинета по url-name
        """
        # Запрос от авторизованного пользователя
        response = self.client.get(reverse("user:account"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_url(self):
        """
        Проверка доступности страницы профайла по url
        """
        # Запрос от авторизованного пользователя
        response = self.client.get("/my/profile/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_name(self):
        """
        Проверка доступности страницы профайла по url-name
        """
        # Запрос от авторизованного пользователя
        response = self.client.get(reverse("user:profile"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_account_url(self):
        """
        Проверка доступности страницы обновления аккаунта по url
        """
        # Запрос от авторизованного пользователя
        response = self.client.get("/my/update_account/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_account_name(self):
        """
        Проверка доступности страницы обновления аккаунта по url-name
        """
        # Запрос от авторизованного пользователя
        response = self.client.get(reverse("user:update_account"), follow=True)
        self.assertEqual(response.status_code, 200)
