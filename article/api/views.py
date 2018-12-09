from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

from article.models import ArticlesPost
from article.api.serializers import (
    ArticleCreateUpdateSerializer,
    ArticleListSerializer,
)

from .permissions import IsOwnerOrReadOnly
from .pagination import ArticlePageNumberPagination


# Create your views here.
# 增
class ArticleCreateAPIView(CreateAPIView):
    queryset = ArticlesPost.objects.all()
    serializer_class = ArticleCreateUpdateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# 删改查
class ArticleUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ArticlesPost.objects.all()
    serializer_class = ArticleCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


# 列表
class ArticleListAPIView(ListAPIView):
    serializer_class = ArticleListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'body', 'author__first_name', 'author__last_name']
    pagination_class = ArticlePageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = ArticlesPost.objects.all()
        query = self.request.GET.get("q")

        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query)
            ).distinct()
        return queryset_list
