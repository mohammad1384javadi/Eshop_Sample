from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home-page'),
    path('about_us', views.AboutUsView.as_view(), name='about-us-page')
]