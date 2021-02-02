from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.http import is_safe_url
from django.contrib import messages
from django.views import View
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.views.generic.edit import FormMixin

from .forms import LoginForm, RegisterForm, GuestForm, EmailReactivationForm
from .models import GuestEmail, EmailActivation
from .signals import user_logged_in_signal
from django.views.generic import CreateView, FormView, DetailView
from ecom.mixins import NextUrlMixin, RequestAttachFormMixin
from django.core.mail import send_mail
from django.template.loader import get_template


# class LoginRequiredMixin(object):
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

@login_required
def user_profile(request):
    return render(request, 'profile.html')


class UserProfile(LoginRequiredMixin, DetailView):
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class AccountEmailActivationView(FormMixin, View):
    success_url = '/login'
    form_class = EmailReactivationForm

    def get(self, request, key=None, *args, **kwargs):
        key = None
        if key is not None:
            self.key = key
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirmed_qs = qs.confirmable()
            if confirmed_qs.count() == 1:
                email_activation_object = confirmed_qs.first()
                email_activation_object.activate()
                messages.success(request, "Success, Your Email Has Been Activate, Proceed To Login")
                return redirect('login')
            else:
                activated_qs = qs.filter(key__iexact=key, activated=True)
                if activated_qs.exists():
                    reset_link = reverse('password_reset')
                    msg = """
                    Your Email Has Already Been Activated...
                    Do You Wish To <a href='{link}'>Reset Your Password?</a>                
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect('login')

        context = {
            'form': self.get_form(),
            'key': key
        }

        return render(request, 'registration/activation_error.html', context)

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """
        Activation Link Sent To Your Email. Check Your Email To Confirm Account.
        
        """
        request = self.request
        messages.success(request, mark_safe(msg))
        email = form.cleaned_data.get('email')
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return AccountEmailActivationView

    def form_invalid(self, form):

        context = {
            'form': form,
            'key': self.key
        }
        return render(self.request, 'registration/activation_error.html', context)


# def register_guest(request):
#     form = GuestForm(request.POST or None)
#
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#
#     if form.is_valid():
#         email = form.cleaned_data.get('email')
#         new_guest_email = GuestEmail.objects.create(email=email)
#         request.session['guest_email_id'] = new_guest_email.id
#
#         if is_safe_url(redirect_path, request.get_host()):
#             return redirect(redirect_path)
#         else:
#             return redirect('register')
#
#     return redirect('register')


class GuestRegisterView(NextUrlMixin, RequestAttachFormMixin, CreateView):
    form_class = GuestForm
    default_next = '/register/'

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)

    # def form_valid(self, form):
    #     request = self.request
    #     email = form.cleaned_data.get('email')
    #     new_guest_email = GuestEmail.objects.create(email=email)
    #     request.session['guest_email_id'] = new_guest_email.id
    #     return redirect(self.get_next_url())


class LoginView(NextUrlMixin, RequestAttachFormMixin, FormView):
    form_class = LoginForm
    template_name = 'login.html'
    default_next = '/'

    def form_valid(self, form):
        request = self.request
        next_path = self.get_next_url()
        return redirect(next_path)


#
# def login_page(request):
#     form = LoginForm(request.POST or None)
#
#     context = {
#         'form': form
#     }
#
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#
#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect('index')
#         else:
#             print('Error')
#
#     return render(request, 'login.html', context)


User = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/accounts/login/'

# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         'form': form
#     }
#
#     if form.is_valid():
#         form.save()
#     return render(request, 'register.html', context)
