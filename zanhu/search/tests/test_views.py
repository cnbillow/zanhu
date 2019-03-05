#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.urls import reverse
from django.test import Client
from test_plus.test import TestCase

from zanhu.articles.models import Article
from zanhu.qa.models import Question
from zanhu.news.models import News


class SearchViewsTests(TestCase):

    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="user01", password="password")
        self.other_client.login(username="user02", password="password")
        self.title = "测试标题"
        self.content = "测试内容"
        # 2篇文章，2个问题，1条动态
        self.article_one = Article.objects.create(
            user=self.user, title="标题1", content=self.content, tags="标签1", status="P"
        )
        self.article_two = Article.objects.create(
            user=self.other_user, title="标题2", content="内容2", tags="标签2", status="P"
        )
        self.question_one = Question.objects.create(
            user=self.user, title="问题1", content="问题1的内容", tags="Python"
        )
        self.question_two = Question.objects.create(
            user=self.user, title="问题2", content="问题2的内容", has_answer=True, tags="Python"
        )
        self.news_one = News.objects.create(user=self.user, content="问题已解决")

    def test_news_search_results(self):
        response = self.client.get(reverse("search:results"), {'query': '问题'})
        assert response.status_code == 200
        assert self.article_one not in response.context["articles_list"]
        assert self.article_two not in response.context["articles_list"]
        assert self.question_one in response.context["questions_list"]
        assert self.question_two in response.context["questions_list"]
        assert self.news_one in response.context["news_list"]
