from core.services import UserService


class AuthMiddlewares:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        try:
            user = UserService.get(f'user/ambassador', headers=request.headers)
        except:
            user = None

        request.user_ms = user

        return self.get_response(request)
