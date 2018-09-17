from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

class ArticleLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 100
    default_limit = 10


class ArticlePageNumberPagination(PageNumberPagination):
    page_size = 10
