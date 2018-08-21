from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponse
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin, StaffuserRequiredMixin

from .forms import AlbumForm
from .models import Album
from utils.utils import PaginatorMixin

from comments.forms import AlbumCommentForm
from comments.models import AlbumComment


# Create your views here.
class AlbumUpload(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    model = Album
    context_object_name = 'album'
    template_name = 'album/album_upload.html'
    fields = ['url', 'title', 'photographer', 'location', 'photo_time', 'camera',
              'lens', 'focal_length', 'aperture', 'exposure_time', 'description']

    def post(self, request, *args, **kwargs):
        forms = AlbumForm(data=request.POST)
        if forms.is_valid():
            new_album = forms.save(commit=False)
            new_album.user = self.request.user
            new_album.save()
            return redirect("album:album_list")
        return self.render_to_response({"forms": forms})


# def album_list(request):
#     album = Album.objects.all()
#     comment_form = AlbumCommentForm()
#     context = {'album': album,
#                'comment_form': comment_form,
#                }
#     return render(request, 'album/album_list.html', context=context)

class AlbumListView(PaginatorMixin, ListView):
    paginate_by = 5
    model = Album
    context_object_name = 'album'
    template_name = 'album/album_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_form = AlbumCommentForm()
        data = {
            'comment_form': comment_form
        }
        context.update(data)
        return context



def album_delete(request, image_id):
    if request.user.is_superuser:
        image = Album.objects.get(id=image_id)
        image.delete()
    return redirect("album:album_list")


def album_manage(request):
    album = Album.objects.all()
    return render(request, 'album/album_manage.html', {'album': album})


