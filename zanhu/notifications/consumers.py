#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationsConsumer(AsyncWebsocketConsumer):
    """处理通知应用中的WebSocket请求"""

    async def connect(self):
        """异步建立连接"""
        if self.scope["user"].is_anonymous:
            # 未登录用户拒绝连接
            await self.close()

        else:
            await self.channel_layer.group_add('notifications', self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        """连接断开"""
        await self.channel_layer.group_discard('notifications', self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """？？？"""
        await self.send(text_data=json.dumps(text_data))
