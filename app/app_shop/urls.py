from django.urls import path, re_path, include

from .views import (
    MainView,
    AboutView,
    ProductsSalesView,
    ProductDetailView,
    ShoppingCartView,
    OrderRegistrationView,
    OrderInformationView,
    HistoryOrderView,
    PaymentView,
    PaymentWithInvoiceGenerationView,
    ProgressPaymentView,
    ProductsListView,
    load_comments,
)

app_name = 'shop'

urlpatterns = [
    path('', MainView.as_view(), name='main'),  # Главная
    path('catalog/', include([  # Фильтрация товаров по категории / тегу, параметрам фильтрации и сортировка
        path('', ProductsListView.as_view(), name='products_list'),
        re_path(r'^(?P<group>.*)/(?P<name>.*)/', ProductsListView.as_view(), name='products_list'),
        re_path(r'^(?P<group>.*)/(?P<name>.*)/.+', ProductsListView.as_view(), name='products_list'),
    ])),
    path('about/', AboutView.as_view(), name='about'),  # О магазине
    path('sale/', ProductsSalesView.as_view(), name='sale'),  # Распродаж
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),  # Страница товара
    path('load_comments/', load_comments, name='load_comments'),  # Загрузка доп.комментариев к товару через кнопку

    # re_path(r'^product/(?P<pk>[0-9]*)/#(?P<tag>.*)', ProductDetailView.as_view(), name='product_detail'),  # Страница товара

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
