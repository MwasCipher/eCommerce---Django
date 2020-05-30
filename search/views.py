from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from products.models import Product


class ProductSearchView(ListView):
    # queryset = Product.objects.all()
    # Custom Model Manager
    template_name = 'search.html'

    def get_context_data(self, object_list=None, *args, **kwargs):
        context = super(ProductSearchView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()
