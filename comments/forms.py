from django import forms
from .models import Comment, AlbumComment, ReadBookComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class AlbumCommentForm(forms.ModelForm):
    class Meta:
        model = AlbumComment
        fields = ['body']


class ReadBookCommentForm(forms.ModelForm):
    class Meta:
        model = ReadBookComment
        fields = ['body']
