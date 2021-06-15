from time import time

from admin_lte.tasks import log_request
from cinema_site.services.middlewares_service import get_client_ip


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        st = time()
        response = self.get_response(request)
        time_execution = time() - st

        path = request.path
        user_ip = get_client_ip(request)
        utm = request.GET.get('utm')

        try:
            referer = request.META.get('HTTP_REFERER')
        except AttributeError:
            referer = None

        ignore_elements = ['/media', '/admin', 'api', 'favicon']
        if not any(element in path for element in ignore_elements):
            log_request.delay(time_execution, path, user_ip, utm, referer)

        return response
