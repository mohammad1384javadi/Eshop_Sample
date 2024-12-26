from django.urls import path
from . import views
from Product_Module.models import Product

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('cat/<category>', views.ProductListView.as_view(), name='product-by-category-list'),
    path('brand/<brand>', views.ProductListView.as_view(), name='product-by-brand-list'),
    # path('favorite_product', views.AddProductFavorite.as_view(), name='favorite-product'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name="product-detail"),
]
