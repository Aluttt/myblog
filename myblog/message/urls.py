from django.urls import path, include

from message import views

urlpatterns = [
    path('post/<int:topic_id>', views.MessageView.as_view()),

]