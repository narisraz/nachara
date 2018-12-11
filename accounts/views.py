from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.utils import translation
from django.conf import settings

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .tokens import account_activation_token 
from .models import User


class AccountsCreate(CreateView):
    model = User
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        form.instance.is_active = False
        user = form.save()
        form.send_email(self.request, user)
        return redirect('accounts-created')

    def post(self, request, *args, **kwargs):
        user_language = request.POST.get('language')
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        return super().post(self, request, *args, **kwargs)


class AccountsDelete(DeleteView):
    model = User
    success_url = reverse_lazy('accounts-add')

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_staff:
            raise PermissionDenied
        current_user = request.user
        user = User.objects.get(pk=kwargs['pk'])
        if current_user.id == user.id:
            return super().delete(self, request, *args, **kwargs)
        raise PermissionDenied

    def render_to_response(self, context, **response_kwargs):
        if self.request.user == context['user'] or self.request.user.is_staff:
            return super().render_to_response(context, **response_kwargs)
        raise PermissionDenied


class AccountsUpdate(UpdateView):
    model = User
    form_class = CustomUserChangeForm

    def get_success_url(self):
        id = self.request.user.id
        return reverse('accounts-detail', args=(id,))

    def render_to_response(self, context, **response_kwargs):
        if self.request.user == context['user'] or self.request.user.is_staff:
            return super().render_to_response(context, **response_kwargs)
        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        user_language = request.POST.get('language')
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        return super().post(self, request, *args, **kwargs)


class AccountsDetail(DetailView):
    model = User
    queryset = User.objects.all()

    def render_to_response(self, context, **response_kwargs):
        print(translation.get_language())
        if self.request.user == context['user'] or self.request.user.is_staff:
            return super().render_to_response(context, **response_kwargs)
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        langDict = { a: b for a, b in settings.LANGUAGES }
        context = super(AccountsDetail, self).get_context_data(**kwargs)
        context['user_language'] = langDict[self.request.user.language]
        return context


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    return render(request, 'account_activation_invalid.html')