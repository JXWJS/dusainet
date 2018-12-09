from django.views.generic import ListView
from utils.utils import PaginatorMixin
from django.urls import reverse


from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from .models import ImageSource

from django.views.generic.edit import FormView
from .forms import ImageUploadForm


# Create your views here.
class ImageSourceListView(PaginatorMixin,
                          LoginRequiredMixin,
                          StaffuserRequiredMixin,
                          ListView,
                          FormView,
                          ):
    """
    图库list
    可批量上传图片
    """
    paginate_by = 10
    model = ImageSource
    template_name = 'imagesource/image_source_list.html'
    context_object_name = 'images'

    # FormView相关
    form_class = ImageUploadForm
    success_url = '/imagesource/imagesource-list'

    def post(self, request, *args, **kwargs):
        """
        处理批量上传的图片
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')

        # 循环存储图片
        if form.is_valid():
            for f in files:
                imagesource = ImageSource(avatar_thumbnail=f)
                imagesource.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
