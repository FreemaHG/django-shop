from django.urls import path, re_path, include
from django.views.decorators.cache import cache_page

# from config.admin import config
from app.config.utils.configuration import get_config
from app.app_shop.views.page import (
    MainView,
    AboutView,
    ProductsSalesView,
)

from .views.products import (
    ProductsLisSearchView,
    ProductsListView,
    ProductDetailView,
)

from .views.request import (
    add_product_in_cart,
    reduce_product,
    increase_product,
    delete_product,
    load_comments,
    add_product,
)

from .views.cart_and_order import (
    ShoppingCartView,
    OrderRegistrationView,
    OrderInformationView,
    HistoryOrderView,
    PaymentView,
    ProgressPaymentView,
)


app_name = "shop"
config = get_config()  # Настройки сайта с параметрами кэширования


urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path(
        "about/",
        cache_page(60 * config.caching_time)(AboutView.as_view()),
        name="about",
    ),
    path(
        "sale/",
        cache_page(60 * config.caching_time)(ProductsSalesView.as_view()),
        name="sale",
    ),
    # Фильтрация товаров по категории / тегу, параметрам фильтрации, сортировка товаров
    path(
        "catalog/",
        include(
            [
                path(
                    "",
                    cache_page(60 * config.caching_time)(ProductsListView.as_view()),
                    name="products_list",
                ),
                re_path(
                    r"^(?P<group>.*)/(?P<name>.*)/.*",
                    ProductsListView.as_view(),
                    name="products_list",
                ),
            ]
        ),
    ),
    # Поиск товаров с фильтрацией и сортировкой результатов
    path(
        "search/",
        include(
            [
                re_path(r"^.*", ProductsLisSearchView.as_view(), name="search"),
            ]
        ),
    ),
    path(
        "product/",
        include(
            [
                path(
                    "<int:pk>", ProductDetailView.as_view(), name="product_detail"
                ),  # Страница товара
                path(
                    "load_comments/", load_comments, name="load_comments"
                ),  # Загрузка доп.комментария (Ajax-запрос)
                path(
                    "add_product/",
                    include(
                        [  # Добавление товара в корзину
                            path("", add_product, name="add_product"),  # Ajax-запрос
                            re_path(
                                r"^(?P<product_id>.*)/next=(?P<next>.*)",
                                add_product_in_cart,
                                name="add_product",
                            ),  # С перезагрузкой страницы
                        ]
                    ),
                ),
                # Удаление товара из корзины (с перезагрузкой страницы)
                re_path(
                    r"^delete_product/(?P<product_id>.*)/next=(?P<next>.*)",
                    delete_product,
                    name="delete_product",
                ),
            ]
        ),
    ),
    # Корзина
    path(
        "shopping_cart/", ShoppingCartView.as_view(), name="shopping_cart"
    ),
    # Уменьшение кол-ва товара в корзине
    path(
        "reduce_product/<int:product_id>", reduce_product, name="reduce_product"
    ),
    # Увеличение кол-ва товара в корзине
    path(
        "increase_product/<int:product_id>", increase_product, name="increase_product"
    ),
    # Заказы
    path(
        "order/",
        include(
            [
                # Регистрация заказа
                path(
                    "registration/",
                    OrderRegistrationView.as_view(),
                    name="order_registration",
                ),
                # История заказов
                path(
                    "history/", HistoryOrderView.as_view(), name="history_order"
                ),
                # Информация о заказе
                path(
                    "detail/<int:pk>",
                    OrderInformationView.as_view(),
                    name="order_detail",
                ),
            ]
        ),
    ),
    # Оплата заказа
    path(
        "payment/",
        include(
            [
                # Онлайн картой
                path(
                    "online/<int:order_id>/",
                    cache_page(60 * config.caching_time)(PaymentView.as_view()),
                    name="online_payment",
                ),
                # Онлайн со случайного чужого счета
                path(
                    "someone/<int:order_id>/",
                    cache_page(60 * config.caching_time)(PaymentView.as_view()),
                    name="someone_payment",
                ),
                # Ожидание оплаты
                path(
                    "progress_payment/<int:order_id>/",
                    cache_page(60 * config.caching_time)(ProgressPaymentView.as_view()),
                    name="progress_payment",
                ),
            ]
        ),
    ),
]
