from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from analytics.mixins import ObjectViewedMixin

# Create your views here.
from .models import Product
from carts.models import Cart


# Class Based View
class ProductFeaturedListView(ListView):
    # queryset = Product.objects.all()
    # Custom Model Manager
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


# Class Based View
class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    template_name = 'products/featured_detail.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


# Class Based View
class ProductListView(ListView):
    template_name = 'products/product_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        request = self.request
        cart_object, new_object = Cart.objects.new_or_getcurrent(request)
        context['cart'] = cart_object
        return context

    # queryset = Product.objects.all()
    # Custom Model Manager
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.order_by('-timestamp')


# Function Based View
def product_list_view(request):
    queryset = Product.objects.all()

    context = {
        'product_list': queryset
    }
    return render(request, 'products/product_list.html', context)


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        request = self.request
        cart_object, new_object = Cart.objects.new_or_getcurrent(request)
        context['cart'] = cart_object
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        product = get_object_or_404(Product, slug=slug)
        try:
            Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404('Item Does Not Exist')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            product = qs.first()
        except:
            raise Http404('Uuumm Awkward!!!')
        # object_viewed_signal.send(product.__class__, instance=product, request=request)
        return product


# Class Based View
class ProductDetailView(ObjectViewedMixin, DetailView):
    # queryset = Product.objects.all()
    template_name = 'products/detail.html'

    # ### Using Custom Model Manager For Class Based View ###
    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')

        product = Product.objects.get_by_id(pk)
        if product is None:
            raise Http404('Product Does Not Exist or Has Been Removed')

        return product

    # ### Can Be Used In Place of get_object() ###
    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)


# Function Based View
def product_detail_view(request, pk, *args, **kwargs):
    # product = get_object_or_404(Product, pk=pk)

    # try:
    #     product = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print('No Product Here')
    #     raise Http404('Product Does Not Exist or Has Been Removed')
    # except:
    #     print('Huh!!!')

    # Using Custom Model Manager To Display Items in Queryset
    product = Product.objects.get_by_id(pk)
    print(product)
    if product is None:
        raise Http404('Product Does Not Exist or Has Been Removed')

    # qs = Product.objects.filter(id=pk)
    # if qs.exists() and qs.count() == 1:
    #     product = qs.first()
    #
    # else:
    #     raise Http404('Product Does Not Exist or Has Been Removed')

    context = {
        'product': product
    }
    return render(request, 'products/detail.html', context)


class UserProductHistoryView(LoginRequiredMixin, ListView):
    template_name = 'products/history.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        request = self.request
        cart_object, new_object = Cart.objects.new_or_getcurrent(request)
        context['cart'] = cart_object
        return context

    # queryset = Product.objects.all()
    # Custom Model Manager
    def get_queryset(self, *args, **kwargs):
        request = self.request
        all_objects_viewed = request.user.objectviewed_set.by_model(Product)
        # products_viewed_IDS = [x.object_id for x in all_objects_viewed]
        return all_objects_viewed
