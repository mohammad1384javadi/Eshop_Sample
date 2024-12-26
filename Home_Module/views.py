from django.db.models import Count, Sum
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView

from Product_Module.models import Product, ProductCategory
from Site_Module.models import SiteSetting, FooterLinkBox, Slider
from utils.convertors import group_list


class HomeView(TemplateView):
    template_name = 'Home_Product/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders: Slider = Slider.objects.filter(is_active=True)
        context['sliders'] = sliders
        latest_product = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]

        most_visit_product = Product.objects.filter(is_active=True, is_delete=False).annotate(visit_count=Count(
            'productvisit')).order_by('productvisit')[:12]

        categories = list(ProductCategory.objects.annotate(
            product_count=Count('product_categories')
        ).filter(is_active=True, is_delete=False, product_count__gt=0)[:4])

        categories_product = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_categories.all())
            }
            categories_product.append(item)

        most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(
            order_count=Sum('orderdetail__count')).order_by('-order_count')[:12]

        context['most_bought_products'] = group_list(most_bought_products)
        context['most_visit_product'] = group_list(most_visit_product)
        context['latest_products'] = group_list(latest_product)
        context['categories_products'] = categories_product
        return context


def site_header_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_active=True).first()
    context = {
        'site_setting': setting
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_active=True).first()
    footer_link_boxes = FooterLinkBox.objects.all()
    context = {
        'site_setting': setting,
        'footer_link_boxes': footer_link_boxes

    }
    return render(request, 'shared/site_footer_component.html', context)


class AboutUsView(TemplateView):
    template_name = 'Home_Product/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True, is_active=True).first()
        context['site_setting'] = site_setting
        return context
