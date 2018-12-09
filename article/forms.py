from django import forms
from django.core.files.base import ContentFile
from .models import ArticlesPost
from uuslug import slugify
from urllib import request


class ArticleCreateForm(forms.ModelForm):
    """
    写新文章的表单
    """
    class Meta:
        model = ArticlesPost
        fields = [
            'title',
            'course_title',
            'column',
            'tags',
            'body',
            'url',
            'course',
            'course_sequence'
        ]

    def clean_url(self):
        """
        获取网络图片的url
        :return: url
        """
        url = self.cleaned_data['url']
        # 检查url的图片格式
        if url:
            valid_extensions = ['jpg', 'jpeg', 'png']
            extension = url.rsplit('.', 1)[1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError("图片格式必须为jpg/jpeg/png.")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """
        重写save(), 修改图片的名字为slug
        :return: 提交的article表单类对象
        """
        article = super(ArticleCreateForm, self).save(commit=False)
        article_url = self.cleaned_data['url']
        if article_url:
            album_name = '{0}.{1}'.format(slugify(article.title), article_url.rsplit('.', 1)[1].lower())
            response = request.urlopen(article_url)
            article.avatar_thumbnail.save(album_name, ContentFile(response.read()), save=False)
        if commit:
            article.save()
        return article
