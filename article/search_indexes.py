from haystack import indexes
from .models import ArticlesPost


class ArticlesPostIndex(indexes.SearchIndex, indexes.Indexable):
    """
    haystack搜索位置
    """
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ArticlesPost

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
