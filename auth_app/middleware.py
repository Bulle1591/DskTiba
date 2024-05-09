from django.utils.deprecation import MiddlewareMixin


class DisableBrowserCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if 'Cache-Control' not in response:
            response['Cache-Control'] = 'no-store'
        return response
