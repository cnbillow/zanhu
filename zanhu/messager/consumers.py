#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MessagesConsumer(AsyncWebsocketConsumer):
    """处理私信应用中的WebSocket请求"""

    async def connect(self):
        """异步建立连接"""
        if self.scope["user"].is_anonymous:
            # 未登录用户拒绝连接
            await self.close()

        else:
            # 加入聊天组（两人私信往来属于一个聊天组）
            await self.channel_layer.group_add(f"{self.scope['user'].username}", self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        # 离开聊天组
        await self.channel_layer.group_discard(f"{self.scope['user'].username}", self.channel_name)

    async def receive(self, text_data):
        """接收私信"""
        await self.send(text_data=json.dumps(text_data))

    # async def receive(self, text_data=None, bytes_data=None):
    #     # 从WebSocket接收消息
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #
    #     # 将消息发送到聊天组
    #     await self.channel_layer.group_send(
    #         f"{self.scope['user'].username}",
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )
    #
    # async def chat_message(self, event):
    #     # 从聊天组接收消息
    #     message = event['message']
    #
    #     # 将消息发送给Websocket
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))
