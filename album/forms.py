from django import forms
from django.core.files.base import ContentFile
from uuslug import slugify
from urllib import request

from .models import Album

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('url', 'title', 'description')

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("图片格式必须为jpg/jpeg/png.")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        album = super(AlbumForm, self).save(commit=False)
        album_url = self.cleaned_data['url']
        album_name = '{0}.{1}'.format(slugify(album.title), album_url.rsplit('.', 1)[1].lower())
        response = request.urlopen(album_url)
        album.image.save(album_name, ContentFile(response.read()), save=False)
        if commit:
            album.save()
        return album