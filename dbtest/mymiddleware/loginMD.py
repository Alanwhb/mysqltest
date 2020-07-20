from django.utils.deprecation import MiddlewareMixin


class TestLogin(MiddlewareMixin):
    def process_request(self, request):
        print("wuhu~")