from django.http import HttpResponse

class rc_factory(object):
    """
    Status codes.
    """
    CODES = dict(ALL_OK = ('OK', 200),
                 CREATED = ('Created', 201),
                 DELETED = ('', 204), # 204 says "Don't send a body!"
                 BAD_REQUEST = ('Bad Request', 400),
                 FORBIDDEN = ('Forbidden', 401),
                 NOT_FOUND = ('Not Found', 404),
                 NOT_ALLOWED = ('Not Allowed', 405),
                 DUPLICATE_ENTRY = ('Conflict/Duplicate', 409),
                 NOT_HERE = ('Gone', 410),
                 NOT_IMPLEMENTED = ('Not Implemented', 501),
                 THROTTLED = ('Throttled', 503))

    def __getattr__(self, attr):
        '''Returns a fresh ``HttpResponse`` when getting an "attribute".'''
        try:
            body, code = self.CODES.get(attr)
        except TypeError:
            raise AttributeError(attr)

        return HttpResponse(body, content_type='text/plain', status=code)

rc = rc_factory()
