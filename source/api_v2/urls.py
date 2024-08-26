from django.urls import path
from .views import ArticleListView, ArticleView, get_token, CommentView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list_create'),
    path('articles/<int:pk>/', ArticleView.as_view()),
    path('token', get_token),
    path('articles/<int:article_pk>/comments/', CommentView.as_view()),
    path('articles/<int:article_pk>/comments/<int:pk>/', CommentView.as_view())
]
