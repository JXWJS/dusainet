from django import forms
from .models import ArticlesPost


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = ArticlesPost
        fields = ['title', 'column', 'tags', 'body']