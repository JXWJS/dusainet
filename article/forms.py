from django import forms
from django.core.files.base import ContentFile
from .models import ArticlesPost
from uuslug import slugify
from urllib import request


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = ArticlesPost
        fields = ['title', 'course_title', 'column', 'tags', 'body', 'url', 'course', 'course_sequence']

    def clean_url(self):
        url = self.cleaned_data['url']
        if url:
            valid_extensions = ['jpg', 'jpeg', 'png']
            extension = url.rsplit('.', 1)[1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError("图片格式必须为jpg/jpeg/png.")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        article = super(ArticleCreateForm, self).save(commit=False)
        article_url = self.cleaned_data['url']
        if article_url:
            album_name = '{0}.{1}'.format(slugify(article.title), article_url.rsplit('.', 1)[1].lower())
            response = request.urlopen(article_url)
            article.avatar_thumbnail.save(album_name, ContentFile(response.read()), save=False)
        if commit:
            article.save()
        return article
