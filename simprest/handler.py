import re
from django.http import HttpResponse
from simprest.emitters import get_emitter
from simprest.utils import rc
from simprest.auth import NoAuth
from simprest.docs import registry

nonalpha_re = re.compile('[^a-z]')

class Rest(object):
    allowed_methods = ('GET', 'PUT', 'POST', 'DELETE')
    params = {}

    def __init__(self, auth=None):
        self.auth = auth or NoAuth()
        registry.register(self)

    def __call__(self, request, *args, **kwargs):
        if not self.auth.is_authenticated(request):
            return self.auth.challenge(request)

        method = nonalpha_re.sub('', request.method.lower())
        if (method.upper() not in self.allowed_methods or
            not hasattr(self, method)):
            return rc.NOT_ALLOWED

        emitter, ct = get_emitter(kwargs.pop('format',
                                             request.GET.get('format')))
        func = getattr(self, method)
        try:
            resp = func(request, *args, **kwargs)
        except Exception, e:
            resp = {'error': unicode(e)}
        if isinstance(resp, HttpResponse):
            return resp

        return HttpResponse(emitter(request, resp), mimetype=ct)
