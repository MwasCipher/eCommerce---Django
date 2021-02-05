# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from .signals import object_viewed_signal
from accounts.signals import user_logged_in_signal
from .utils import get_user_ip

# Create your models here.

User = settings.AUTH_USER_MODEL


class ObjectViewedQuerySet(models.query.QuerySet):
    def by_model(self, model_class):
        con_type = ContentType.objects.get_for_model(model_class)
        return self.filter(content_type=con_type)


class ObjectViewedManager(models.Manager):
    def get_queryset(self):
        return ObjectViewedQuerySet(self.model, using=self._db)

    def by_model(self, model_class):
        return self.get_queryset().by_model(model_class)


class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ObjectViewedManager()

    def __str__(self):
        return "%s Viewed %s" % (self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    con_type = ContentType.objects.get_for_model(sender)  # Content Type

    ObjectViewed.objects.create(user=request.user, object_id=instance.id, content_type=con_type,
                                ip_address=get_user_ip(request))


object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    session_key = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.session_key)

    def end_session(self):
        ended = self.ended
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return ended


# def post_save_session_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
#         for i in qs:
#             i.end_session()
#
#     if not instance.active and instance.ended:
#         instance.end_session()
#
#
# post_save.connect(post_save_session_receiver, sender=UserSession)
#
#
# def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)
#         for i in qs:
#             i.end_session()
#
#
# post_save.connect(post_save_user_changed_receiver, sender=User)


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    print(instance)
    user = instance
    session_key = request.session.session_key
    ip_address = get_user_ip(request)

    UserSession.objects.create(user=user, ip_address=ip_address, session_key=session_key)


user_logged_in_signal.connect(user_logged_in_receiver)
