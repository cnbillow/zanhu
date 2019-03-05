#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.test import Client
from django.urls import reverse
from test_plus.test import TestCase

from zanhu.qa.models import Question, Answer


class QAViewsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="user01", password="password")
        self.other_client.login(username="user02", password="password")
        self.question_one = Question.objects.create(
            user=self.user,
            title="问题1",
            content="问题1的内容",
            tags="测试1, 测试2"
        )
        self.question_two = Question.objects.create(
            user=self.user,
            title="问题2",
            content="问题2的内容",
            has_answer=True,
            tags="测试1, 测试2"
        )
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question_two,
            content="问题2被采纳的回答",
            is_answer=True
        )

    def test_index_questions(self):
        response = self.client.get(reverse("qa:all_q"))
        assert response.status_code == 200
        assert "问题1" in str(response.context["questions"])

    def test_create_question_view(self):
        current_count = Question.objects.count()
        response = self.client.post(reverse("qa:ask_question"),
                                    {"title": "问题标题",
                                     "content": "问题内容",
                                     "status": "O",
                                     "tags": "测试标签"})
        assert response.status_code == 302
        new_question = Question.objects.first()
        assert new_question.title == "问题标题"
        assert Question.objects.count() == current_count + 1

    def test_answered_questions(self):
        response = self.client.get(reverse("qa:answered_q"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("问题2" in str(response.context["questions"]))

    def test_unanswered_questions(self):
        response = self.client.get(reverse("qa:unanswered_q"))
        assert response.status_code == 200
        assert "问题1" in str(response.context["questions"])

    def test_answer_question(self):
        current_answer_count = Answer.objects.count()
        response = self.client.post(
            reverse("qa:propose_answer", kwargs={"question_id": self.question_one.id}), {"content": "问题1的回答"}
        )
        assert response.status_code == 302
        assert Answer.objects.count() == current_answer_count + 1

    def test_question_upvote(self):
        """赞同问题"""
        response_one = self.client.post(
            reverse("qa:question_vote"),
            {"value": "U", "question": self.question_one.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        assert response_one.status_code == 200

    def test_question_downvote(self):
        """反对问题"""
        response_one = self.client.post(
            reverse("qa:question_vote"),
            {"value": "D", "question": self.question_one.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_answer_upvote(self):
        """赞同回答"""
        response_one = self.client.post(
            reverse("qa:answer_vote"),
            {"value": "U", "answer": self.answer.uuid_id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_answer_downvote(self):
        """反对回答"""
        response_one = self.client.post(
            reverse("qa:answer_vote"),
            {"value": "D", "answer": self.answer.uuid_id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_accept_answer(self):
        """接受回答"""
        response_one = self.client.post(
            reverse("qa:accept_answer"),
            {"answer": self.answer.uuid_id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200
