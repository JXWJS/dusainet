from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from .forms import AlbumForm
from .models import Album
from utils.utils import PaginatorMixin


# Create your views here.
class AlbumUpload(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    """
    上传图片的视图
    未开发完成，不建议使用
    暂用admin代替
    """
    model = Album
    context_object_name = 'album'
    template_name = 'album/album_upload.html'
    fields = ['url', 'title', 'description']

    def post(self, request, *args, **kwargs):
        forms = AlbumForm(data=request.POST)
        if forms.is_valid():
            new_album = forms.save(commit=False)
            new_album.user = self.request.user
            new_album.save()
            return redirect("album:album_list")
        return self.render_to_response({"forms": forms})


class AlbumListView(PaginatorMixin, ListView):
    """
    album list主页面
    """
    paginate_by = 20
    model = Album
    context_object_name = 'album'
    template_name = 'album/album_list.html'


def album_delete(request, image_id):
    """
    删除图片
    未开发，暂用admin代替
    :param request:
    :param image_id: 图片的id
    :return: 重定向到album list模板
    """
    if request.user.is_superuser:
        image = Album.objects.get(id=image_id)
        image.delete()
    return redirect("album:album_list")


def album_manage(request):
    """
    album管理页面
    未开发，暂用admin代替
    :param request:
    :return: 管理页面模板
    """
    album = Album.objects.all()
    return render(request, 'album/album_manage.html', {'album': album})
