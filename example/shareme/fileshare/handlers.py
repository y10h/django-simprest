from django import forms
from simprest import Rest, rc

from fileshare.models import File

def only_single_file(view):
    def wrap(self, request):
        if len(request.FILES) != 1:
            return rc.BAD_REQUEST
        return view(self, request)
    return wrap


def absolute_reverse(request, *args, **kwargs):
    from django.core.urlresolvers import reverse

    path = reverse(*args, **kwargs)
    return request.build_absolute_uri(path)


def absolute_media(request, media_path):
    from django.conf import settings

    path = '/'.join((
            '',
            settings.MEDIA_URL.strip('/'),
            media_path.lstrip('/')))

    return request.build_absolute_uri(path)


def serialize(request, obj):
    return {
        'id': obj.id,
        'title': obj.title,
        'content_url': absolute_media(request, obj.content.name),
        'self_url': absolute_reverse(request, 'get_file', args=[obj.id])}

class NewFile(Rest):
    """
    Create new file. Request should be form-multidata encoded.

    methods: POST
    params:
        * <any_field> --- content of uploading file.
    returns: JSON object
    """

    @only_single_file
    def post(self, request):
        key = request.FILES.keys()[0]
        obj = File.objects.create(
            content=request.FILES[key],
            title=key,)
        return serialize(request, obj)


class GetFile(Rest):
    """
    Get existing file object.

    methods: GET
    returns: JSON object
    """
    def get(self, request, id):
        try:
            obj = File.objects.get(pk=id)
        except File.DoesnotExist:
            return rc.NOT_FOUND
        return serialize(request, obj)
