#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from zanhu.messager.models import Message
from zanhu.helpers import ajax_required


class MessagesListView(LoginRequiredMixin, ListView):
    model = Message
    paginate_by = 20
    template_name = "messager/message_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MessagesListView, self).get_context_data(*args, **kwargs)
        # 获取除当前登录用户外的所有用户，按最近登录时间降序排列
        context['users_list'] = get_user_model().objects.filter(
            is_active=True).exclude(username=self.request.user).order_by('-last_login')
        # 最近一次私信互动的用户
        last_conversation = Message.objects.get_most_recent_conversation(self.request.user)
        context['active'] = last_conversation.username
        return context

    def get_queryset(self):
        """最近一次私信互动的内容"""
        active_user = Message.objects.get_most_recent_conversation(self.request.user)
        return Message.objects.get_conversation(active_user, self.request.user)


class ConversationListView(MessagesListView):
    """与指定用户的私信内容"""

    def get_context_data(self, *args, **kwargs):
        context = super(ConversationListView, self).get_context_data(*args, **kwargs)
        context['active'] = self.kwargs["username"]
        return context

    def get_queryset(self):
        active_user = get_object_or_404(get_user_model(), username=self.kwargs["username"])
        return Message.objects.get_conversation(active_user, self.request.user)


@login_required
@ajax_required
@require_http_methods(["POST"])
def send_message(request):
    """发送消息，AJAX POST请求"""
    sender = request.user
    recipient_username = request.POST.get('to')
    recipient = get_user_model().objects.get(username=recipient_username)
    message = request.POST.get('message')
    # 内容不为空且不是发送给自己
    if len(message.strip()) != 0 and sender != recipient:
        msg = Message.objects.create(
            sender=sender,
            recipient=recipient,
            message=message
        )  # 程序执行到这一步，并没有在数据库中真正写入数据

        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'message',
            'message_id': str(msg.uuid_id),
            'sender': sender.username,
            'recipient': recipient.username
        }
        async_to_sync(channel_layer.group_send)(recipient.username, payload)

        return render(request, 'messager/single_message.html', {'message': msg})

    return HttpResponse()


@login_required
@ajax_required
@require_http_methods(["GET"])
def receive_message(request):
    """接收消息，AJAX GET请求"""
    message_id = request.GET.get('message_id')
    msg = Message.objects.get(pk=message_id)
    return render(request, 'messager/single_message.html', {'message': msg})
