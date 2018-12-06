from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
  path('add/', views.AccountsCreate.as_view(), name='accounts-add'),
  path('created/', TemplateView.as_view(template_name='accounts/user_created.html'), name='accounts-created'),
  path('<int:pk>/', views.AccountsDetail.as_view(), name='accounts-detail'),
  path('<int:pk>/update/', views.AccountsUpdate.as_view(), name='accounts-update'),
  path('<int:pk>/delete/', views.AccountsDelete.as_view(), name='accounts-delete'),
  path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
  url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]
