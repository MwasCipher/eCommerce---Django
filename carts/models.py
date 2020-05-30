from django.db import models
from products.models import Product
from django.conf import settings

from django.db.models.signals import pre_save, post_save, m2m_changed
from decimal import Decimal

# Create your models here.
User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_getcurrent(self, request):
        cart_id = request.session.get('cart_id', None)

        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_object = False
            print('Cart Exists....#@#@#@#@#@#@#@#@#@#@#@#@#@#@#')
            cart_object = qs.first()
            if request.user.is_authenticated() and cart_object.user is None:
                cart_object.user = request.user
                cart_object.save()
        else:
            cart_object = Cart.objects.create_new_cart(user=request.user)
            new_object = True
            request.session['cart_id'] = cart_object.id

        return cart_object, new_object

    def create_new_cart(self, user=None):
        user_object = None
        if user is not None:
            if user.is_authenticated():
                user_object = user

        return self.model.objects.create(user=user_object)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def cart_m2m_changed_receiver(instance, action, sender, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(cart_m2m_changed_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal) + Decimal(1.08)
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)
