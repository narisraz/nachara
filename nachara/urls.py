from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static, serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('oauth/', include('social_django.urls', namespace='social')),
    url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        })
]
