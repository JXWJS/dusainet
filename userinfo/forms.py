from django import forms
from .models import UserInfo

from PIL import Image
from django import forms
from django.core.files import File
from .models import UserInfo


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['avatar']


class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = UserInfo
        fields = (
            'avatar',
            'x',
            'y',
            'width',
            'height',
        )

    def save(self, commit=True, user_id=None):

        if UserInfo.objects.get(user_id=user_id):
            userinfo = UserInfo.objects.get(user_id=user_id)
            userinfo.avatar = super(PhotoForm, self).save(commit=False).avatar
        else:
            userinfo = super(PhotoForm, self).save(commit=False)
            userinfo.user_id = user_id

        userinfo.save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(userinfo.avatar)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((150, 150), Image.ANTIALIAS)
        resized_image.save(userinfo.avatar.path)

        return userinfo
