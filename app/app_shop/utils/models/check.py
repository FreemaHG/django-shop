from ...models import CategoryProduct, Product


def active_products(category: CategoryProduct) -> bool:
    """
    Проверка наличия активных товаров в категории
    """
    ...

# # TODO не используется нигде
# def free_shipping(product: Product, threshold_cost: 2000) -> bool:
#     """
#     Проверка бесплатной доставки для товара
#     (доставка бесплатная, если стоимость товара больше порогового значения, по умолчанию 2000 руб)
#     """
#     if product.price > threshold_cost:
#         return True
#     return False