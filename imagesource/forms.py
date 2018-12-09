from django import forms

class ImageUploadForm(forms.Form):
    file_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))