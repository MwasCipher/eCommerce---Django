from django.conf.urls import url

from .views import ProductSearchView

urlpatterns = [
    url(r'^$', ProductSearchView.as_view(), name='search'),
]
