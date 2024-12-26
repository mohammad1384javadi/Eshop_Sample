from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article, ArticleCategory, ArticleComments


# Create your views here.

class ArticleListView(ListView):
    template_name = 'Article_Module/article-list.html'
    model = Article
    paginate_by = 4

    def get_queryset(self):
        query = super().get_queryset()
        category_name = self.kwargs.get('category')
        query = query.filter(is_active=True)
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query


class ArticleDetailView(DetailView):
    template_name = 'Article_Module/article_detail.html'
    model = Article

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article: Article = kwargs.get('object')
        context['comments'] = ArticleComments.objects.filter(article_id=article.id, parent_id=None).order_by(
            '-create_date').prefetch_related('articlecomments_set')
        context['all_comments'] = ArticleComments.objects.filter(article_id=article.id).count()
        return context


def article_category_component(request):
    article_main_category = ArticleCategory.objects.filter(is_active=True, parent_id=None)
    context = {
        'article_main_category': article_main_category
    }
    return render(request, 'Article_Module/component/article_category_component.html', context)


def add_article_comment(request):
    if request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_comment = request.GET.get('article_comment')
        parent_id = request.GET.get('parent_id')
        new_comment = ArticleComments(
            article_id=article_id,
            text=article_comment,
            user_id=request.user.id,
            parent_id=parent_id
        )
        new_comment.save()
        context = {
            'comments': ArticleComments.objects.filter(article_id=article_id, parent_id=None).order_by(
                '-create_date').prefetch_related('articlecomments_set'),
            'all_comments': ArticleComments.objects.filter(article_id=article_id).count()
        }
        return render(request, 'Article_Module/includes/article_comments_partial.html', context)
    return HttpResponse('response')
