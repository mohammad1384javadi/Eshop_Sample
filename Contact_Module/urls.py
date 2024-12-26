from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactUsView.as_view(), name='contact_us_page'),
    path('create-profile/', views.CreateProfileView.as_view(), name='create-profile-page'),
    path('profiles/', views.ProfileListView.as_view(), name='profiles-page')
]