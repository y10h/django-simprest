from django.core.urlresolvers import get_resolver
from django.http import HttpResponse

class HandlerRegistry(dict):
    def __init__(self):
        self.maxlength = 0

    def __setitem__(self, name, value):
        self.maxlength = max(self.maxlength, len(str(value)))
        super(HandlerRegistry, self).__setitem__(name, value)

    def register(self, handler):
        self[handler] = None

    def sync_urls(self):
        resolver = get_resolver(None)
        reverse = resolver.reverse_dict
        for h in self:
            if not self[h]:
                # tied to current django url storage
                urltuple = reverse[h][0][0]
                args = dict((name, '<%s>' % name) for name in urltuple[1])
                url = urltuple[0] % args
                self[h] = url

registry = HandlerRegistry()

def docs(request):
    registry.sync_urls()
    output = []
    format = '%%-%ss\n%%s\n\n' % registry.maxlength
    paramformatsrc = '\t%%-%ss - %%s\n'
    for handler, url in registry.items():
        try:
            paramlength = max(map(len, handler.params.keys()))
            paramformat = paramformatsrc % paramlength
            params = ''.join(paramformat % (k, v) for k, v
                             in handler.params.items())
        except ValueError:
            params = ''
        if handler.__doc__:
            doc = '\t%s\n\n%s' % (handler.__doc__.strip(), params)
        else:
            doc = params
        output.append(format % (url, doc))
    return HttpResponse(''.join(output), mimetype='text/plain')
