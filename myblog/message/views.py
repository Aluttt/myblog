import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from message.models import MessageModel
from tools.chack_login import check_login
from topic.models import TopicModel
#10400 - 499

class MessageView(View):


    @method_decorator(check_login)
    def post(self, request, topic_id):
        json_str = request.body
        json_obj = json.loads(json_str)
        content = json_obj['content']
        try:
            parent_id = json_obj['parent_id']

        except:
            parent_id = 0
        visitor = request.user

        try:
            topic = TopicModel.objects.get(id=topic_id)
        except:
            return JsonResponse({'code':10400})


        MessageModel.objects.create(content=content, publisher_id=visitor, topic_id=topic, parent_message=parent_id)

        return JsonResponse({'code':200})

