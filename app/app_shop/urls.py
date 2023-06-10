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
    add_product,
    add_product_in_cart,
    reduce_product,
    increase_product,
    delete_product,
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
    path('product/', include([
        path('<int:pk>', ProductDetailView.as_view(), name='product_detail'),  # Страница товара
        path('load_comments/', load_comments, name='load_comments'),  # Загрузка доп.комментариев к товару через кнопку

        # FIXME Объединить add_product через include
        # Добавление товара в корзину
        path('add_product/', add_product, name='add_product'),  # Ajax-запрос
        re_path(r'^add_product/(?P<product_id>.*)/next=(?P<next>.*)', add_product_in_cart, name='add_product'),  # С перезагрузкой страницы

        # Удаление товара из корзины
        re_path(r'^delete_product/(?P<product_id>.*)/next=(?P<next>.*)', delete_product, name='delete_product'),  # С перезагрузкой страницы
    ])),

    # re_path(r'^product/(?P<pk>[0-9]*)/#(?P<tag>.*)', ProductDetailView.as_view(), name='product_detail'),  # Страница товара

    path('shopping_cart/', ShoppingCartView.as_view(), name='shopping_cart'),  # Корзина с товарами
    # path('shopping_cart/#<int:id_product>', ShoppingCartView.as_view(), name='shopping_cart'),  # Корзина с товарами
    re_path(r'^shopping_cart/#(?P<id_product>.*)', ShoppingCartView.as_view(), name='shopping_cart'),  # С перезагрузкой страницы

    path('reduce_product/<int:product_id>', reduce_product, name='reduce_product'),      # Уменьшение кол-ва товара в корзине
    path('increase_product/<int:product_id>', increase_product, name='increase_product'),      # Увеличение кол-ва товара в корзине

    path('order/', include([
        path('registration/', include([
            # TODO Вернуть на уровень выше!
            path('', OrderRegistrationView.as_view(), name='order_registration'),
        ])),

        path('information/', OrderInformationView.as_view(), name='order_information'),  # Информация о заказе
        path('history/', HistoryOrderView.as_view(), name='history_order'),  # История заказов
        path('payment/', PaymentView.as_view(), name='order_payment'),  # Оплата заказа
        path(
            'payment_with_invoice_generation/', PaymentWithInvoiceGenerationView.as_view(),
            name='payment_with_invoice_generation'),  # Оплата заказа с генерацией случайного счета
        path('progress_payment/', ProgressPaymentView.as_view(), name='progress_payment'),  # Ожидание оплаты
    ])),
]
