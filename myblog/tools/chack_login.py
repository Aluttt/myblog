#获取request中token请求头 jwt解码 取出token中用户名 返回request.user模型类对象
from django.conf import settings
from django.http import JsonResponse
import jwt

from user.models import UserModel


def check_login(func):
    def wrap(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({'code':403, 'error':'please login'})

        try:
            data = jwt.decode(token, settings.JWT_TOKEN_KEY, 'HS256')
        except Exception as e:
            return JsonResponse({'code':403, 'error':'please login'})
        nickname = data['data']['username']
        user = UserModel.objects.get(nickname=nickname)
        request.user = user
        return func(request, *args, **kwargs)
    return wrap

def get_request_username(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    try:
        data = jwt.decode(token, settings.JWT_TOKEN_KEY, 'HS256')
        visitor = data['data']['username']
    except:
        pass
    return visitor