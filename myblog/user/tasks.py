from django.core.cache import cache

from myblog.celery import app
import random


from tools.get_sms_celery import YunTongXin

@app.task
def get_sms_task(phonenum):

    code = ''

    for i in range(4):
        code += str(random.randint(0,9))

    cache.set(phonenum, code, 180)

    config = {
        'accountSid':'8a216da8806f31ad0180adf3afab0e02',
        'appId':'8a216da8806f31ad0180adf3b0b30e08',
        'accountToken':'be430fe228fd45c298f5a73970b82e0d',
        'templates':'1'
    }

    r = YunTongXin(**config)
    res = r.run(code, phonenum)
    print(res)
    return res

