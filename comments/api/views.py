from django.db.models import Q
from django.contrib.auth.models import User

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.mixins import (
    DestroyModelMixin,
    UpdateModelMixin,
)

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
)

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

from comments.models import Comment
from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    CommentCreateSerializer,
)

from article.models import ArticlesPost
from .permissions import IsOwnerOrReadOnly
from article.api.pagination import ArticlePageNumberPagination


# Create your views here.
# 增
class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(
            article=ArticlesPost.objects.get(id=self.request.GET.get("article_id")),
            reply_to=User.objects.filter(id=self.request.GET.get("reply_to")).first(),
            parent=Comment.objects.filter(id=self.request.GET.get("parent")).first(),
            user=self.request.user,
        )


# 删改查
class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['body']
    pagination_class = ArticlePageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.all()
        query = self.request.GET.get("q")

        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query)
            ).distinct()
        return queryset_list
