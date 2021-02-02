from django.utils.http import is_safe_url

class RequestAttachFormMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestAttachFormMixin, self).get_form_kwargs()
        print(kwargs)
        kwargs['request'] = self.request
        return kwargs
class NextUrlMixin(object):

    def get_next_url(self):
        default_next = 'index'
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        if is_safe_url(redirect_path, request.get_host()):
            return redirect_path
        return self.default_next
