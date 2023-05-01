from django.urls import path, include

from .views import (
    MainView,
    ProductsListView,
    ProductsFilterListView,
    ProductsForTagLIstView,
    ResetFiltersView,
    AboutView,
    ProductsSalesView,
    ProductDetailView,
    ShoppingCartView,
    OrderRegistrationView,
    OrderInformationView,
    HistoryOrderView,
    PaymentView,
    PaymentWithInvoiceGenerationView,
    ProductsSortedByPrice,
    ProgressPaymentView,
)

app_name = 'shop'

urlpatterns = [
    path('', MainView.as_view(), name='main'),  # Главная
    path('catalog/', include([
        path('', ProductsListView.as_view(), name='products_list'),
        path('category/<slug:category_name>', ProductsListView.as_view(), name='products_list'),
        path('tags/<slug:tag_name>', ProductsForTagLIstView.as_view(), name='filter_by_tags'),
        path('filter/', include([
            path('', ProductsFilterListView.as_view(), name='products_filter_list'),  # Вывод отфильтрованных товаров
            path('reset/', ResetFiltersView.as_view(), name='reset_filters'),  # Сброс параметров фильтрации
        ])),
        path('sorted/', include([
            # path('by_popularity/', name='sorted_by_popularity'),  # Сортировка товаров по популярности
            path('by_price/', ProductsSortedByPrice.as_view(), name='sorted_by_price'),  # Сортировка товаров по цене
            # path('by_reviews/', name='sorted_by_reviews'),  # Сортировка товаров по кол-ву отзывов
            # path('by_novelty/', name='sorted_by_novelty'),  # Сортировка товаров по новизне
        ])),
    ])),
    path('about/', AboutView.as_view(), name='about'),  # О магазине
    path('sale/', ProductsSalesView.as_view(), name='sale'),  # Распродаж
    path('product/', ProductDetailView.as_view(), name='product'),  # Страница товара
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
