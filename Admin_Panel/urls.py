from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='_admin_index_page'),
    path('articles/', views.ArticleListView.as_view(), name='_admin_article_list_page'),
    path('articles/edit/<pk>', views.ArticleEditView.as_view(), name='_admin_article_edit_page')
]