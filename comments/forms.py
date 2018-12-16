from django import forms
from .models import Comment, ReadBookComment, VlogComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class ReadBookCommentForm(forms.ModelForm):
    class Meta:
        model = ReadBookComment
        fields = ['body']

class VlogCommentForm(forms.ModelForm):
    class Meta:
        model = VlogComment
        fields = ['body']
