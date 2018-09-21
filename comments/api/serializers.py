from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from comments.models import Comment


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'body',
        ]


class CommentListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api_comments:detail'
    )
    article = SerializerMethodField()
    user = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'url',
            'id',
            'article',
            'user',
            'body',
        ]

    def get_article(self, obj):
        return obj.article.title

    def get_user(self, obj):
        return obj.user.username


class CommentDetailSerializer(ModelSerializer):
    article_url = SerializerMethodField()
    user = SerializerMethodField()
    reply_to = SerializerMethodField()
    article = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'article_url',
            'article',
            'id',
            'user',
            'reply_to',
            'body',
            'created_time',
        ]

    def get_article_url(self, obj):
        return obj.article.get_api_url()

    def get_article(self, obj):
        return obj.article.title

    def get_user(self, obj):
        return obj.user.username

    def get_reply_to(self, obj):
        try:
            result = obj.reply_to.username
        except:
            result = None
        return result


class CommentForArticleSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api_comments:detail'
    )
    user = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'url',
            'id',
            'user',
            'body',
        ]

    def get_user(self, obj):
        return obj.user.username
