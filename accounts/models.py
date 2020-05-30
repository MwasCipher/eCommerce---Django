from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('User Must Have A Working Email Address!!!')
        if not password:
            raise ValueError('Password is Required')
        if not full_name:
            raise ValueError('User Must Enter Full Name!!!')
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

    @property
    def is_active(self):
        return self.active


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
