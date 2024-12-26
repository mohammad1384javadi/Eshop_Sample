from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from Site_Module.models import SiteBanner
from utils.convertors import group_list
from utils.http_service import get_client_ip
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView, DetailView


# Create your views here.


# class ProductListView(TemplateView):
#     template_name = 'Product_Module/product_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.all().order_by('price')
#         return context


class ProductListView(ListView):
    template_name = 'Product_Module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        query = Product.objects.all()
        product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or 16000000
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_list)
        return context

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True, is_delete=False)
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)
        if end_price is not None:
            query = query.filter(price__lte=end_price)

        category_name = self.kwargs.get('category')
        brand_name = self.kwargs.get('brand')
        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query


class ProductDetailView(DetailView):
    template_name = 'Product_Module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        # favorite_product_id = request.session.get('product_favorite')
        # context['is_favorite'] = str(loaded_product.id) == favorite_product_id
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_detail)
        galleries = list(ProductGallery.objects.filter(is_active=True, product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        context['product_galleries_group'] = group_list(galleries, 3)
        user_ip = get_client_ip(self.request)
        context['related_products'] = group_list(list(
            Product.objects.filter(
                is_active=True, brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all()[:12]
            )
        )
        user_id = None
        if request.user.is_authenticated:
            user_id = request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit_product = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit_product.save()
        return context


class AddProductFavorite(View):
    def post(self, request):
        product_id = request.POST["product_id"]
        product = Product.objects.get(pk=product_id)
        request.session["product_favorite"] = product_id
        return redirect(product.get_absolute_url())


# class ProductDetailView(TemplateView):
#     template_name = 'Product_Module/product_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         slug = kwargs['slug']
#         product = get_object_or_404(Product, slug=slug)
#         context['product'] = product
#         return context

# def product_list(request):
#     products = Product.objects.all().order_by("price")
#     return render(request, 'Product_Module/product_list.html', {
#         "products": products
#     })


# def product_detail(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     return render(request, 'Product_Module/product_detail.html', {
#         "product": product
#     })

def product_category_component(request):
    context = {
        'categories': ProductCategory.objects.filter(is_active=True, is_delete=False)
    }
    return render(request, 'Product_Module/components/product_categories_component.html', context)


def product_brand_component(request):
    product_brand = ProductBrand.objects.annotate(product_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brand
    }
    return render(request, 'Product_Module/components/product_brand_component.html', context)
