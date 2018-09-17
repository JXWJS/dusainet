from rest_framework.serializers import (
    ModelSerializer,
    ReadOnlyField,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from article.models import ArticlesPost


# from comment.serializers import CommentListSerializer, CommentDetailSerializer
# from comment.models import Comment

# from account.serializers import UserDetailSerializer


class ArticleCreateUpdateSerializer(ModelSerializer):
    author = SerializerMethodField()

    class Meta:
        model = ArticlesPost
        fields = [
            'author',
            'title',
            'course_title',
            'column',
            'course',
            'course_sequence',
            # 'tags',
            'body',
            'created',
        ]

    def get_author(self, obj):
        return str(obj.author)


class ArticleDetailSerializer(ModelSerializer):
    # author = UserDetailSerializer(read_only=True)
    # comments = SerializerMethodField()
    author = SerializerMethodField()

    class Meta:
        model = ArticlesPost
        fields = [
            'id',
            'author',
            'title',
            'body',
            # 'comments',
        ]

    # def get_comments(self, obj):
    #     c_qs = Comment.objects.filter(article=obj.id)
    #     comments = CommentListSerializer(c_qs, many=True, context=self.context).data
    #     return comments

    def get_author(self, obj):
        return str(obj.author)


class ArticleListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api_article:detail',
    )
    # author = UserDetailSerializer(read_only=True)
    author = SerializerMethodField()
    column = SerializerMethodField()
    course = SerializerMethodField()

    # tags = SerializerMethodField()

    class Meta:
        model = ArticlesPost
        fields = [
            'url',
            'id',
            'author',
            'title',
            'course_title',
            'column',
            'course',
            # 'tags',
            'total_views',
        ]

    def get_author(self, obj):
        return str(obj.author)

    def get_column(self, obj):
        if obj.column:
            return str(obj.column)
        else:
            return None

    def get_course(self, obj):
        if obj.course:
            return str(obj.course)
        else:
            return None

    # def get_tags(self, obj):
    #     if obj.tags:
    #         return str(obj.tags.slug)
    #     else:
    #         return None
