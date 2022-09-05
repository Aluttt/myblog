from django.db import models

from topic.models import TopicModel
from user.models import UserModel


class MessageModel(models.Model):
    content = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    parent_message = models.IntegerField()
    publisher_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    topic_id = models.ForeignKey(TopicModel, on_delete=models.CASCADE)
# Create your models here.
