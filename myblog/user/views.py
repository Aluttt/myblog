import json
import hashlib
import time

from django.core.cache import cache
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from tools.chack_login import check_login
from .tasks import get_sms_task
from django.shortcuts import render

# Create your views here.
from django.views import View

from myblog import settings
from .models import UserModel
#10100-10199
class UserViews(View):

    @method_decorator(check_login)
    def get(self, request, nickname):
        nickname = request.user.nickname
        avatar = request.user.avatar
        sign = request.user.sign

        return JsonResponse({'code':200, 'data':{'nickname':nickname, 'avatar':str(avatar), 'sign':sign}})


    @method_decorator(check_login)
    def put(self, request, nickname):
        json_obj = request.body
        json_str = json.loads(json_obj)
        nickname = json_str['nickname']
        sign = json_str['sign']
        user = request.user
        user.nickname = nickname
        user.sign = sign
        user.save()
        return JsonResponse({'code':200, 'data':{'nickname':nickname, 'sign':sign}})


    def post(self, request):
        json_obj = request.body
        json_str = json.loads(json_obj)
        phone = json_str['phonenum']
        nickname = json_str['nickname']
        email = json_str['email']
        sms_num = json_str['sms_num']
        password_1 = json_str['password_1']
        password_2 = json_str['password_2']
        if password_1 != password_2:
            return JsonResponse({'code':10100})

        have_phone = UserModel.objects.filter(phone=phone)
        if have_phone:
            return JsonResponse({'code': 10101, 'error': '该号码已被注册'})

        have_nickname = UserModel.objects.filter(nickname=nickname)
        if have_nickname:
            return JsonResponse({'code': 10102, 'error': '用户名已被注册'})

        have_sms = cache.get(phone)
        if not have_sms:
            return JsonResponse({'code': 10103})
        if have_sms != sms_num:
            return JsonResponse({'code':10104})


        m = hashlib.md5()
        m.update(password_1.encode())


        UserModel.objects.create(nickname=nickname, password=m.hexdigest(), email=email, phone=phone )
        return JsonResponse({'code':200, 'nickname':nickname})


def get_sms(request):
    json_obj = request.body
    json_str = json.loads(json_obj)
    phonenum = json_str['phonenum']


    get_sms_task.delay(phonenum)
    return JsonResponse({'code':200 })

@check_login
def chang_avatar(request, nickname):
    img = request.FILES['avatar']
    user = request.user
    user.avatar = img
    user.save()

    return JsonResponse({'code':200})

@check_login
def chang_password(request, nickname):
    json_obj = request.body
    json_str = json.loads(json_obj)
    phone = json_str['phonenum']
    password = json_str['password']
    sms_num = json_str['sms_num']

    user = request.user
    if user.phone != phone:
        return JsonResponse({'error':'phone error'})

    have_sms = cache.get(phone)
    if not have_sms:
        return JsonResponse({'code': 10103})
    if have_sms != sms_num:
        return JsonResponse({'code': 10104})

    m = hashlib.md5()
    m.update(password.encode())

    user.password = m.hexdigest()
    user.save()
    return JsonResponse({'code':200, 'nickname':nickname})