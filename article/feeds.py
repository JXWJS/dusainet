from django.contrib.syndication.views import Feed

from .models import ArticlesPost, ArticlesColumn


class ArticlesPostRssFeed(Feed):
    # 通过聚合阅读器跳转到网站的地址
    link = "/"

    # 显示在聚合阅读器上的描述信息
    description = "关于编程、摄影和生活"

    # 显示在聚合阅读器上的标题
    def title(self, obj):
        return "杜赛的博客文章"

    # 需要显示的内容条目
    def items(self):
        return ArticlesPost.objects.all()

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.column, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body


class ArticlesPostColumnRssFeed(ArticlesPostRssFeed):

    def get_object(self, request, column_id):
        return ArticlesColumn.objects.get(pk=column_id)

    def title(self, obj):
        return "杜赛的[%s]博客文章" % obj.title

    def items(self, obj):
        return ArticlesPost.objects.filter(column=obj)
