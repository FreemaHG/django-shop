from django.urls import path, include

from .views import (
    MainView,
    AboutView,
    ProductsSalesView,
    ProductDetailView,
    CatalogView,
    ShoppingCartView,
    OrderRegistrationView,
    OrderInformationView,
    HistoryOrderView,
    PaymentView,
    PaymentWithInvoiceGenerationView,
    ProgressPaymentView,
)

urlpatterns = [
    path('', MainView.as_view(), name='main'),  # Главная
    path('about/', AboutView.as_view(), name='about'),  # О магазине
    path('sale/', ProductsSalesView.as_view(), name='sale'),  # Распродаж
    path('product/', ProductDetailView.as_view(), name='product'),  # Страница товара
    path('catalog/', CatalogView.as_view(), name='catalog'),  # Каталог товаров
    path('shopping_cart/', ShoppingCartView.as_view(), name='shopping_cart'),  # Корзина с товарами
    path('order/', include([
        path('registration/', OrderRegistrationView.as_view(), name='order_registration'),  # Регистрация заказа
        path('information/', OrderInformationView.as_view(), name='order_information'),  # Информация о заказе
        path('history/', HistoryOrderView.as_view(), name='history_order'),  # История заказов
        path('payment/', PaymentView.as_view(), name='order_payment'),  # Оплата заказа
        path(
            'payment_with_invoice_generation/', PaymentWithInvoiceGenerationView.as_view(),
            name='payment_with_invoice_generation'),  # Оплата заказа с генерацией случайного счета
        path('progress_payment/', ProgressPaymentView.as_view(), name='progress_payment'),  # Ожидание оплаты
    ])),
]
