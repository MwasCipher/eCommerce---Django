from django.conf.urls import url

from .views import (ProductListView,
                    # product_list_view,
                    # product_detail_view,
                    # ProductDetailView,
                    ProductDetailSlugView,
                    # ProductFeaturedListView,
                    # ProductFeaturedDetailView
                    )


urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='products'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='product'),
]
