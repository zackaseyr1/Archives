from django.http import HttpResponseForbidden

class BlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.block:
            response = HttpResponseForbidden('<div style="text-align: center;"><h1>You are blocked from accessing this website.</h1></div>')
            response["Content-Type"] = "text/html"
            return response

        return self.get_response(request)
