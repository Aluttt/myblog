import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from message.models import MessageModel
from tools.chack_login import check_login, get_request_username
from topic.models import TopicModel
#10300-10399
from user.models import UserModel


class TopicViews(View):

    #自己看自己 is_self = True 显示私有文章  category = tec or no-tec 显示技术类or非技术类 无此字段 全部显示
    def make_topics_res(self, username, topic):
        res = {'code':200, 'data':{}}
        topic_list = []

        for i in topic:
            d = {}
            d['id'] = i.id
            d['title'] = i.title
            d['category'] = i.category
            d['created_time'] = i.created_time.strftime('%Y-%m-%d %H:%M')
            d['content'] = i.content
            d['introduce'] = i.introduce
            d['author'] = username
            topic_list.append(d)

        res['data']['nickname'] = username
        res['data']['topics'] = topic_list
        return res

    def make_topic_res(self, is_self, username, topic):


        #messages and reply

        messages = MessageModel.objects.filter(topic_id=topic.id).order_by('-created_time')
        msg_dic = {}
        msg_list = []
        msg_count = 0
        for message in messages:
            msg_count += 1
            parent_msg = messages.filter(id=message.parent_message)
            sender = UserModel.objects.get(id=message.publisher_id_id)
            if parent_msg:
                reply_dic = {}
                msg_dic.setdefault(message.parent_message, [])

                reply_dic['publisher'] = sender.nickname
                reply_dic['publisher_avatar'] = str(sender.avatar)
                reply_dic['created_time'] = message.created_time.strftime('%Y-%m-%d %H:%M')
                reply_dic['content'] = message.content
                reply_dic['msg_id'] = message.id
                msg_dic[message.parent_message].append(reply_dic)
            else:

                msg_list.append({
                    'id':message.id,
                    'content':message.content,
                    'publisher': sender.nickname,
                    'publisher_avatar': str(sender.avatar),
                    'created_time': message.created_time.strftime('%Y-%m-%d %H:%M'),
                    'reply': [],
                })
                # {
                #  id: 2
                #  reply [
                #  {msg_id:1, parent_id:2, }
                #  {msg_id:2, parent_id:2. }
                #  ]
                #
                # }
                #  {
                #  2 : [{msg:1,par:2},{msg:2,par:2}],
                #  3 : [],
                #  4 : [{msg:2,par:2}]
                #  }
        for i in msg_list:
            if i['id'] in msg_dic:
                i['reply'] = msg_dic[i['id']]


        res = {'code': 200, 'data': {}}

        if is_self:
            next_topic = TopicModel.objects.filter(id__gt=topic.id).first()
            last_topic = TopicModel.objects.filter(id__lt=topic.id).last()
        else:
            next_topic = TopicModel.objects.filter(id__gt=topic.id, limit='public').first()
            last_topic = TopicModel.objects.filter(id__lt=topic.id, limit='public').last()


        res['data']['nickname'] = username
        res['data']['title'] = topic.title
        res['data']['category'] = topic.category
        res['data']['created_time'] = topic.created_time.strftime('%Y-%m-%d %H:%M')
        res['data']['content'] = topic.content
        res['data']['introduce'] = topic.introduce
        res['data']['author'] = username
        res['data']['next_id'] = next_topic.id if next_topic else None
        res['data']['next_title'] = next_topic.title if next_topic else ''
        res['data']['last_id'] = last_topic.id if last_topic else None
        res['data']['last_title'] = last_topic.title if last_topic else ''
        res['data']['messages'] = msg_list
        res['data']['messages_count'] = msg_count

        return res

    def get(self, request, username):
        try:
            UserModel.objects.get(nickname=username)
        except:
            return JsonResponse({'code':301, 'error':'no author'})
        is_self = False
        category = request.GET.get('category')
        visitor = get_request_username(request)

        if visitor:
            user = UserModel.objects.get(nickname=visitor)


        if visitor == username:
            is_self = True


        #詳情頁查詢
        t_id = request.GET.get('t_id')
        if t_id:
            if is_self:
                try:
                    topic = TopicModel.objects.get(id=t_id)
                except:
                    return JsonResponse({'error': '查無此文'})
                res = self.make_topic_res(is_self, username, topic)
                return JsonResponse(res)
            else:
                try:
                    topic = TopicModel.objects.get(id=t_id, limit='public')
                except:
                    return JsonResponse({'error': '查無此文'})
                res = self.make_topic_res(is_self, username, topic)
                return JsonResponse(res)

        #技術類查詢
        if category:
            if is_self:
                topic = TopicModel.objects.filter(author=user.id, category=category)
                res = self.make_topics_res(username, topic)
                return JsonResponse(res)
            else:
                topic = TopicModel.objects.filter(author=user.id, category=category, limit='public')
                res = self.make_topics_res(username, topic)
                return JsonResponse(res)
        #全部查詢
        if is_self:
            topic = TopicModel.objects.filter(author=user.id)
            res = self.make_topics_res(username, topic)
            return JsonResponse(res)
        else:
            topic = TopicModel.objects.filter(author=user.id, limit='public')
            res = self.make_topics_res(username, topic)
            return JsonResponse(res)

        if category not in ['tec','no-tec']:
            return JsonResponse({'code': 10302})
        if category not in ['tec', 'no-tec']:
            return JsonResponse({'error': 'run'})



    @method_decorator(check_login)
    def post(self, request, username):
        username = request.user.nickname

        json_str = request.body
        json_obj = json.loads(json_str)

        content = json_obj['content']
        title = json_obj['title']
        category = json_obj['category']
        limit = json_obj['limit']
        introduce = content[:30]

        if category not in ['tec','no-tec']:
            return JsonResponse({'code':10300})

        if limit not in ['public','private']:
            return JsonResponse({'code': 10301})


        TopicModel.objects.create(title=title, content=content, category=category, limit=limit, introduce=introduce, author_id=request.user.id)

        return JsonResponse({'code':200, 'username':username})