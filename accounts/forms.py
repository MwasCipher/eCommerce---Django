from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import EmailActivation, GuestEmail
from .signals import user_logged_in_signal

User = get_user_model()


class EmailReactivationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse('register')
            msg = """
                This Email Does Nt Exist, Proceed To Register
                Would You Like To <a href='{link}'>Register?</a>                     
                """.format(link=register_link)
            messages.success(mark_safe(msg))
            raise forms.ValidationError("")
        return email


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin', 'full_name')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class GuestForm(forms.ModelForm):
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    class Meta:
        model = GuestEmail
        fields = [
            'email'
        ]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GuestForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        # Save the provided password in hashed format
        obj = super(UserAdminCreationForm, self).save(commit=False)
        if commit:
            obj.save()
            request = self.request
            request.session['guest_email_id'] = obj.id
        return obj


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email',
                                                            'name': 'email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'name': 'password',
                                                                 'class': 'form-control'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')

        link = 'resend_activation'
        resend_confirmation_msg = """
        Click <a href='{resend_link}' >Here </a>To Resend Activation Link
        """.format(link)

        qs = User.objects.filter(email=email)
        if qs.exists():

            not_active = qs.filter(is_active=False)
            if not_active.exists():

                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    resend_msg = "Please Check Your email To Confirm Your Account!!! " \
                                 + mark_safe(resend_confirmation_msg)
                    raise forms.ValidationError(resend_msg)
                confirm_email_exists = EmailActivation.objects.email_exists(email).exists()
                if confirm_email_exists:
                    raise forms.ValidationError(mark_safe(resend_confirmation_msg))
                if not is_confirmable and not confirm_email_exists:
                    raise forms.ValidationError("This User Is InActive!!!")

        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Incorrect Credentials!!!")
        login(request, user)
        self.user = user
        user_logged_in_signal.send(user.__class__, instance=user, request=request)

        try:
            del request.session['guest_email_id']
        except:
            pass

    # def form_valid(self, form):
    #     msg = """
    #     Activation Link Sent To Your Email. Check Your Email To Confirm Account.
    #
    #     """
    #     request = self.request
    #     messages.success(request, mark_safe(msg))
    #     email = form.cleaned_data.get('email')
    #     obj = EmailActivation.objects.email_exists(email).first()
    #     user = obj.user
    #     new_activation = EmailActivation.objects.create(user=user, email=email)
    #     new_activation.send_activation()
    #     return AccountEmailActivationView
    #
    # def form_invalid(self, form):
    #     context = {
    #         'form': form,
    #         'key': self.key
    #     }
    #     return render(self.request, 'registration/activation_error.html', context)


class RegisterForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'full_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False  # Send confirmation email using signals

        if commit:
            user.save()
        return user


class UserDetailsUpdateForm(forms.ModelForm):
    full_name = forms.CharField(label='Name', required=False)
    class Meta:
        model = User
        fields = [
            'full_name'
        ]
