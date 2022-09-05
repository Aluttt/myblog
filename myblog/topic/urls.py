from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from topic import views

urlpatterns = [
    path('post/<str:username>', views.TopicViews.as_view()),
    path('get/<str:username>', views.TopicViews.as_view()),

]