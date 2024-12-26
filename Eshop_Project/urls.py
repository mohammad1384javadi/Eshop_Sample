"""
URL configuration for Eshop_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home_Module.urls')),
    path('articles/', include('Article_Module.urls')),
    path('', include('Account_Module.urls')),
    path('contact-us/', include('Contact_Module.urls')),
    path('order/', include('Order_Module.urls')),
    path('products/', include('Product_Module.urls')),
    path('user/', include('User_Panel_Module.urls')),
    path('admin-panel/', include('Admin_Panel.urls'))
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
