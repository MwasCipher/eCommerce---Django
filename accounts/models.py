from random import randint

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import pre_save, post_save
from ecom.utils import random_string_generator, unique_verification_key_generator

# Create your models here.
from django.template.loader import get_template
from datetime import timedelta
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('User Must Have A Working Email Address!!!')
        if not password:
            raise ValueError('Password is Required')

        user_object = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_object.set_password(password)
        user_object.staff = is_staff
        user_object.admin = is_admin
        user_object.active = is_active
        user_object.save(using=self._db)
        return user_object

    def create_staffuser(self, email, full_name=None, password=None):
        staff_user = self.create_user(email, full_name=full_name, password=password, is_staff=True)
        return staff_user

    def create_superuser(self, email, full_name=None, password=None):
        super_user = self.create_user(email, full_name=full_name, password=password, is_staff=True, is_admin=True)
        return super_user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255, default='john@doe.com')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.active


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class EmailActivationQueryset(models.query.QuerySet):
    def confirmable(self):
        return self.filter(
            activated=False,
            forced_expire=False
        )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        current_date_time = timezone.now()
        return EmailActivationQueryset(self.model, using=self._db)


class EmailActivation(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField()
    key = models.CharField(max_length=120, null=True, blank=True)
    activated = models.BooleanField(default=False)
    forced_expire = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)  # Expires in 7 Days
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return False
        return True

    def send_activation(self):
        base_url = getattr(settings, 'BASE_URL')
        path_key = self.key
        path = '{base_url}{path}'.format(base_url=base_url, path=path_key)
        if not self.activated and not self.forced_expire:

            if self.key:
                context = {
                    'path': '',
                    'email': self.email
                }

                verify_text = get_template('registration/emails/verify.txt').render(context)
                verify_page_html = get_template('registration/emails/verify.html').render(context)
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [self.email, from_email]
                verify_mail = send_mail(
                    subject='',
                    message=verify_text,
                    from_email='',
                    recipient_list='',
                    html_message=verify_page_html,
                    fail_silently=False
                )
                return verify_mail

        return False


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expire:
        if not instance.key:
            # key_length = randint(30, 45)
            # key = random_string_generator(size=key_length)
            # qs = EmailActivation.objects.filter(key__iexact=key)
            # if qs.exists():
            #     key = random_string_generator(size=key_length)
            instance.key = unique_verification_key_generator(instance)


pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_create_user_receiver(instance, sender, created, *args, **kwargs):
    if created:
        activation_object = EmailActivation.objects.create(user=instance, email=instance.email)
        activation_object.send_activation()


post_save.connect(post_save_create_user_receiver, sender=User)
