from http.client import HTTPResponse

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v2.serializers.article import ArticleSerializer
from api_v2.serializers.comment import CommentSerializer
from webapp.models import Article, Comment
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def get_token(request):
    if request.method == 'GET':
        return HTTPResponse()


class ArticleListView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id

        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class ArticleView(APIView):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response({'id': pk}, status=status.HTTP_204_NO_CONTENT)


class CommentView(APIView):
    def get(self, request, article_pk=None, pk=None):
        if pk:
            comment = get_object_or_404(Comment, pk=pk, article_id=article_pk)
            serializer = CommentSerializer(comment, exclude_likes=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            comments = Comment.objects.filter(article_id=article_pk)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_pk):
        if not request.user.is_authenticated:
            return Response({"detail": "error"}, status=status.HTTP_403_FORBIDDEN)

        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(article=article, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, article_pk, pk):
        comment = get_object_or_404(Comment, pk=pk, article_id=article_pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_pk, pk):
        comment = get_object_or_404(Comment, pk=pk, article_id=article_pk)
        comment.delete()
        return Response({'id': pk}, status=status.HTTP_204_NO_CONTENT)