#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.urls import path

from zanhu.articles import views

app_name = 'articles'  # Django > 2.0，这样模板中可以使用"{% url 'articles:list' %}"，"articles"是总urls.py中定义的namespace

urlpatterns = [
    path('', views.ArticlesListView.as_view(), name='list'),
    path('write-new-article/', views.CreateArticleView.as_view(), name='write_new'),
    path('drafts/', views.DraftsListView.as_view(), name='drafts'),
    path('edit/<int:pk>/', views.EditArticleView.as_view(), name='edit_article'),
    path('<slug>/', views.DetailArticleView.as_view(), name='article'),
]
