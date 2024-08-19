from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, View

from webapp.forms import CommentForm
from webapp.models import Article, Comment


class CreateCommentView(LoginRequiredMixin, CreateView):
    template_name = "comments/create_comment.html"
    form_class = CommentForm

    # def form_valid(self, form):
    #     article = get_object_or_404(Article, pk=self.kwargs['pk'])
    #     form.instance.article = article
    #     return super().form_valid(form)

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.article = article
        comment.author = self.request.user
        comment.save()
        return redirect(article.get_absolute_url())

    # def get_success_url(self):
    #     return reverse("webapp:article_detail", kwargs={"pk": self.object.article.pk})


class UpdateCommentView(UpdateView):
    template_name = "comments/update_comment.html"
    form_class = CommentForm
    model = Comment

    def get_success_url(self):
        return reverse("webapp:article_detail", kwargs={"pk": self.object.article.pk})


class DeleteCommentView(DeleteView):
    queryset = Comment.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("webapp:article_detail", pk=self.object.article.pk)


class LikeCommentView(LoginRequiredMixin, View):
    def get(self, request, *args, article_pk, pk, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        liked = request.user in comment.like_users.all()
        if liked:
            comment.like_users.remove(request.user)
            liked = False
        else:
            comment.like_users.add(request.user)
            liked = True
        comment.update_like_count()
        data = {
            'liked': liked,
            'like_count': comment.like_users.count()
        }
        return JsonResponse(data)