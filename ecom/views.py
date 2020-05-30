from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import ContactForm, LoginForm, RegisterForm


def home_page(request):
    context = {
        'title': 'Hello World'
    }
    return render(request, 'pages/home_page.html', context)


def about_page(request):

    return render(request, 'pages/home_page.html')


def contact_page(request):
    contact_form = ContactForm(request.POST or None)

    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({'message': 'Thank You'})

    if contact_form.errors:
        print(contact_form.cleaned_data)
        contact_form_errors = contact_form.errors().as_json()
        if request.is_ajax():
            return HttpResponse(contact_form_errors, status=400, content_type='application/json')

    context = {
        'form': contact_form
    }
    return render(request, 'pages/contact.html', context)


# def login_page(request):
#     form = LoginForm(request.POST or None)
#
#     context = {
#         'form': form
#     }
#
#     if form.is_valid():
#         print(form.cleaned_data)
#         print(request.user.is_authenticated())
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             print(request.user.is_authenticated())
#             return redirect('login')
#
#     return render(request, 'accounts/login.html', context)

#
# User = get_user_model()


# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         'form': form
#     }
#
#     if form.is_valid():
#         form.save()
#     return render(request, 'accounts/register.html', context)
