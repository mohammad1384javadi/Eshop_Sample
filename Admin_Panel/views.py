from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, UpdateView
from Article_Module.models import Article
from utils.my_decorators import permission_checker_decorator_factory


@method_decorator(permission_checker_decorator_factory('this is my data'), 'dispatch')
class HomeView(TemplateView):
    template_name = 'Admin_Panel/home/index.html'


@method_decorator(permission_checker_decorator_factory(), 'dispatch')
class ArticleListView(ListView):
    model = Article
    template_name = 'Admin_Panel/articles/articles_list.html'
    paginate_by = 12


@method_decorator(permission_checker_decorator_factory(), 'dispatch')
class ArticleEditView(UpdateView):
    model = Article
    template_name = 'Admin_Panel/articles/edit_articles.html'
    fields = '__all__'
    success_url = reverse_lazy('_admin_article_list_page')
