#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.urls import path

from zanhu.search import views

app_name = 'search'

urlpatterns = [
    path('', views.SearchListView.as_view(), name='results'),
]
