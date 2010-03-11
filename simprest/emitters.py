try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.utils import simplejson
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.encoding import smart_unicode

EMITTERS = {}

def get_emitter(format):
    try:
        return EMITTERS[format]
    except KeyError:
        raise ValueError('No emitter registered for type %s' % format)

def register_emitter(name=None, content_type='text/plain'):
    '''Decorator to register an emitter.

    Parameters::

     - ``name``: name of emitter ('json', 'xml', ...)
     - ``content_type``: content type to serve response as
    '''
    def inner(func):
        EMITTERS[name or func.__name__] = (func, content_type)
    return inner


@register_emitter(content_type='application/json; charset=utf-8')
def json(request, data):
    cb = request.GET.get('callback')
    data = simplejson.dumps(data, cls=DateTimeAwareJSONEncoder,
                            ensure_ascii=False, indent=4)
    return cb and ('%s(%s)' % (cb, data)) or data


@register_emitter(content_type='text/xml; charset=utf-8')
def xml(request, data):
    stream = StringIO()
    xml = SimplerXMLGenerator(stream, 'utf-8')
    xml.startDocument()
    xml.startElement('response', {})
    to_xml(xml, data)
    xml.endElement('response')
    xml.endDocument()
    return stream.getvalue()

def to_xml(xml, data):
    if isinstance(data, (list, tuple)):
        for item in data:
            xml.startElement('resource', {})
            to_xml(xml, item)
            xml.endElement('resource')
    elif isinstance(data, dict):
        for key, value in data.iteritems():
            xml.startElement(key, {})
            to_xml(xml, value)
            xml.endElement(key)
    else:
        xml.characters(smart_unicode(data))
