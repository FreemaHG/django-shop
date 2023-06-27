import logging

from django.views.generic import TemplateView

from ..services.main import ProductsForMainService


logger = logging.getLogger(__name__)


class MainView(TemplateView):
    """
    Представление для вывода главной страницы сайта
    """

    template_name = "../templates/app_shop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = ProductsForMainService.save_data(
            context=context, request=self.request
        )

        return context


class AboutView(TemplateView):
    """
    Представление для вывода страницы с информацией о магазине
    """

    template_name = "../templates/app_shop/about.html"


class ProductsSalesView(TemplateView):
    """
    Представление для вывода страницы блога
    """

    template_name = "../templates/app_shop/sale.html"
