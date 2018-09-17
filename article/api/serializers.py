from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)

from article.models import ArticlesPost

from comments.api.serializers import CommentForArticleSerializer
from comments.models import Comment


class ArticleCreateUpdateSerializer(ModelSerializer):
    comments = SerializerMethodField()
    column_r = SerializerMethodField()
    course_r = SerializerMethodField()

    class Meta:
        model = ArticlesPost
        fields = [
            'title',
            'course_title',
            'column',
            'course',
            'column_r',
            'course_r',
            'course_sequence',
            'body',
            'created',
            'comments',
        ]
        read_only_fields = [
            'created',
        ]
        extra_kwargs = {
            'course_sequence': {'write_only': True},
            'column': {'write_only': True},
            'course': {'write_only': True},
        }

    def get_comments(self, obj):
        c_qs = Comment.objects.filter(article=obj.id)
        comments = CommentForArticleSerializer(c_qs, many=True, context=self.context).data
        return comments

    def get_column_r(self, obj):
        try:
            result = obj.column.title
        except:
            result = None
        return result

    def get_course_r(self, obj):
        try:
            result = obj.course.title
        except:
            result = None
        return result


class ArticleListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='api_article:detail',
    )
    column = SerializerMethodField()
    course = SerializerMethodField()
    comment_counts = SerializerMethodField()

    class Meta:
        model = ArticlesPost
        fields = [
            'url',
            'title',
            'column',
            'course',
            'comment_counts',
            'total_views',
        ]

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

    def get_comment_counts(self, obj):
        c_qs = Comment.objects.filter(article=obj.id)
        return c_qs.count()
