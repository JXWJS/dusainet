from django import forms
from .models import Comment, AlbumComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class AlbumCommentForm(forms.ModelForm):
    class Meta:
        model = AlbumComment
        fields = ['body']