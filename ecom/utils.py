import random
import string
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


print(random_string_generator())

print(random_string_generator(size=50))

'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''


def unique_order_id_generator(instance):
    """
    This is for a Django project and it assumes your instance
    has a model with an order_id field
    """
    new_order_id = random_string_generator().upper()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=new_order_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return new_order_id


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_verification_key_generator(instance):
    """
    This is for a Django project and it assumes your instance
    has a model with a key field
    """
    key_length = random.randint(30, 45)
    new_verification_key = random_string_generator(size=key_length).upper()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=new_verification_key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return new_verification_key
