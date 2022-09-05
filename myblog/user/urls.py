from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from user import views

urlpatterns = [
    path('post/', views.UserViews.as_view()),
    path('post/<str:nickname>', views.UserViews.as_view()),
    path('get/<str:nickname>', views.UserViews.as_view()),
    path('post/<str:nickname>/avatar', views.chang_avatar),
    path('put/<str:nickname>', views.UserViews.as_view()),
    path('put/<str:nickname>/password', views.chang_password),
    path('get/sms', views.get_sms)
]