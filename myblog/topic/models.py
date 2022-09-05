from django.db import models
from user.models import UserModel
class TopicModel(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    limit = models.CharField(max_length=10)
    introduce = models.CharField(max_length=90)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
# Create your models here.
