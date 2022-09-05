from django.db import models
import random
def default_sign():
    signs = ['过去终究是过去，过去的遗憾不能填补。','我也是人，我也会累的呢，别把我对你的在乎，随意践踏。', '如果你让一个女孩笑了，她会喜欢你。但是你要是让她哭了，她就是爱你。', '我要一年一年安安静静陪你过，直到变老']
    return random.choice(signs)
class UserModel(models.Model):
    nickname = models.CharField(max_length=11, unique=True, db_index=True ,verbose_name='昵称')
    password = models.CharField(max_length=32, verbose_name='密码')
    sign = models.CharField(max_length=32,default=default_sign, verbose_name='个性签名')
    avatar = models.ImageField(upload_to='avatar',null=True)
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(max_length=11, unique=True, verbose_name='电话号码')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    #info = models.CharField(max_length=)
# Create your models here.
