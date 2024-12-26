from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserPanelDashboardView.as_view(), name='user_panel_page'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile_page'),
    path('user_basket/', views.user_basket, name='user_basket_page'),
    path('remove_order_detail/', views.remove_order_detail, name='remove_order_detail_page'),
    path('change_order_detail/', views.change_order_detail_count, name='change_order_detail_page'),
    path('my-shopping/', views.UserShoppingView.as_view(), name='user_shopping_list'),
    path('my-shopping-detail/<order_id>', views.user_shopping_detail, name='user_shopping_detail'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password_page')
]