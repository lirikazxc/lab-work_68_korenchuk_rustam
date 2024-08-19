from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from webapp.forms import ArticleForm, SearchForm
from webapp.models import Article


class ArticleListView(ListView):
    # queryset = Article.objects.filter(title__contains="Стат")
    model = Article
    template_name = "articles/index.html"
    ordering = ['-created_at']
    context_object_name = "articles"
    paginate_by = 5

    # paginate_orphans = 2

    def dispatch(self, request, *args, **kwargs):
        print(request.user.is_authenticated, "is_authenticated")
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        form = self.form
        if form.is_valid():
            return form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(title__contains=self.search_value) | Q(author__contains=self.search_value)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = context['object_list']
        user = self.request.user

        if user.is_authenticated:
            for article in articles:
                article.user_liked = article.like_users.filter(id=user.id).exists()
                article.like_count = article.like_users.count()
        else:
            for article in articles:
                article.user_liked = False

        context['articles'] = articles
        context["search_form"] = self.form
        if self.search_value:
            context["search"] = urlencode({"search": self.search_value})
            context["search_value"] = self.search_value
        return context


class CreateArticleView(LoginRequiredMixin, CreateView):
    template_name = "articles/create_article.html"
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleDetailView(DetailView):
    template_name = "articles/article_detail.html"
    model = Article

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.order_by("-created_at")
        return context


class UpdateArticleView(PermissionRequiredMixin, UpdateView):
    template_name = "articles/update_article.html"
    form_class = ArticleForm
    model = Article
    permission_required = "webapp.change_article"

    def has_permission(self):
        # return self.request.user.groups.filter(name="moderators").exists()
        return super().has_permission() or self.request.user == self.get_object().author


class DeleteArticleView(PermissionRequiredMixin, DeleteView):
    template_name = "articles/delete_article.html"
    model = Article
    success_url = reverse_lazy("webapp:articles")
    permission_required = "webapp.delete_article"

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class LikeArticleView(LoginRequiredMixin, View):
    def get(self, request, *args, pk, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if request.user in article.like_users.all():
            article.like_users.remove(request.user)
            liked = False
        else:
            article.like_users.add(request.user)
            liked = True

        article.update_like_count()
        data = {
            'liked': liked,
            'like_count': article.like_users.count()
        }
        return JsonResponse(data)