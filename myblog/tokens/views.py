import hashlib
import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import jwt
import datetime
#10200-10299
# Create your views here.
from user.models import UserModel


def new_tokens(username):

    dic = {
        'exp': datetime.datetime.now() + datetime.timedelta(days=1),
        'iat': datetime.datetime.now(),
        'data':{
            'username': username
        }
    }

    s = jwt.encode(dic, settings.JWT_TOKEN_KEY, 'HS256')
    return s


def login_tokens(request):
    if request.method != 'POST':
        return JsonResponse({'code':10200})

    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    password = json_obj['password']

    try:
        user = UserModel.objects.get(nickname=username)
    except Exception as e:
        return JsonResponse({'code':10201, 'error':'no user'})

    m = hashlib.md5()
    m.update(password.encode())

    if user.password != m.hexdigest():
        return JsonResponse({'code':10202, 'error':'用户名或密码错误'})

    token = new_tokens(username)
    return JsonResponse({'code':200, 'username':username, 'data':{'token':token}})