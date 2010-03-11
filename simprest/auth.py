class NoAuth(object):
    def is_authenticated(self, request):
        return True
