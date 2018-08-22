"""dusainet2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from article.views import ArticlePostView
from article.feeds import ArticlesPostRssFeed, ArticlesPostColumnRssFeed
import notifications.urls


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS

    path('admin/', admin.site.urls),
    url(r'^$', ArticlePostView.as_view(), name='home'),
    path('admiration/', TemplateView.as_view(template_name='admiration.html'), name='admiration'),

    path('article/', include('article.urls', namespace='article')),
    url(r'comments/', include('comments.urls', namespace='comments')),
    path('album/', include('album.urls', namespace='album')),
    path('course/', include('course.urls', namespace='course')),
    path('readbook/', include('readbook.urls', namespace='readbook')),
    path('imagesource/', include('imagesource.urls', namespace='imagesource')),
    path('aboutme/', include('aboutme.urls', namespace='aboutme')),
    path('my-notifications/', include('mynotifications.urls', namespace='my_notifications')),

    # RSS订阅
    url(r'^all/rss/$', ArticlesPostRssFeed(), name='rss'),
    path('all/rss/<int:column_id>/', ArticlesPostColumnRssFeed(), name='column_rss'),

    # haystack search
    url(r'^search/', include('haystack.urls')),

    # allauth
    path('accounts/', include('allauth.urls')),

    path('account/weibo_login_success/', TemplateView.as_view(template_name='account/weibo_login_success.html')),

    # notifications
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
