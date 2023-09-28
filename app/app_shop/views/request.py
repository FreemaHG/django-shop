import logging

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect

from app.app_shop.services.products.detail_page import ProductCommentsService
from app.app_shop.services.shop_cart.logic import CartProductsService


logger = logging.getLogger(__name__)


def load_comments(request):
    """
    Обработка запроса для загрузки доп.комментариев к товару
    """
    comments_obj = ProductCommentsService.load_comment(request=request)
    data = {"comments": comments_obj}

    return JsonResponse(data=data)


def add_product(request):
    """
    Обработка Ajax-запроса на добавление товара в корзину
    """
    logger.debug("Добавление товара в корзину (Ajax-запрос)")
    res = CartProductsService.add(request=request)
    data = {"res": res}

    return JsonResponse(data=data)


def add_product_in_cart(request, **kwargs):
    """
    Обработка запроса на добавление товара в корзину (с перезагрузкой страницы)
    """
    logger.debug("Добавление товара в корзину (с обновлением страницы)")
    CartProductsService.add(request=request, product_id=kwargs["product_id"])

    return HttpResponseRedirect(kwargs["next"])


def delete_product(request, **kwargs):
    """
    Обработка запроса на удаление товара из корзины
    """
    logger.debug("Удаление товара из корзины")
    CartProductsService.delete(request=request, product_id=kwargs["product_id"])

    return HttpResponseRedirect(kwargs["next"])


def reduce_product(request, **kwargs):
    """
    Обработка запроса на уменьшение кол-ва товара в корзине
    """
    product_id = kwargs["product_id"]
    logger.debug(f"Уменьшение кол-ва товара в корзине: id - {product_id}")
    CartProductsService.reduce_product(request=request, product_id=product_id)

    return redirect("{}#{}".format(reverse("shop:shopping_cart"), product_id))


def increase_product(request, **kwargs):
    """
    Обработка запроса на увеличение кол-ва товара в корзине
    """
    product_id = kwargs["product_id"]
    logger.debug(f"Увеличение кол-ва товара в корзине: id - {product_id}")
    CartProductsService.increase_product(request=request, product_id=product_id)

    return redirect("{}#{}".format(reverse("shop:shopping_cart"), product_id))
