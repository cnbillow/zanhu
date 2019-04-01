#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView

from taggit.models import Tag

from zanhu.articles.models import Article
from zanhu.news.models import News
from zanhu.qa.models import Question


class SearchListView(LoginRequiredMixin, ListView):
    model = Article  # News或Question
    template_name = "search/search_results.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchListView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get("query", "")
        if not query:
            return context
        # 文章
        context["articles_list"] = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query), status="P"
        )
        # 首页
        context["news_list"] = News.objects.filter(content__icontains=query, reply=False)
        # 问题
        context["questions_list"] = Question.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        # 用户
        context["users_list"] = get_user_model().objects.filter(
            Q(username__icontains=query) | Q(nickname__icontains=query)
        )
        # 标签
        context["tags_list"] = Tag.objects.filter(name=query)
        # 以上数量统计
        context["tags_count"] = context["tags_list"].count()
        context["news_count"] = context["news_list"].count()
        context["articles_count"] = context["articles_list"].count()
        context["questions_count"] = context["questions_list"].count()
        context["users_count"] = context["users_list"].count()

        return context
