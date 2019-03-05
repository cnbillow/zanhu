#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from test_plus.test import TestCase

from zanhu.qa.models import Question, Answer


class QAModelsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")
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
            content="问题2的正确回答",
            is_answer=True
        )

    def test_can_vote_question(self):
        """给问题投票"""
        self.question_one.votes.update_or_create(user=self.user, defaults={"value": True}, )
        self.question_one.votes.update_or_create(user=self.other_user, defaults={"value": True})
        self.question_one.count_votes()
        assert self.question_one.total_votes == 2  # user01与user02各投一票

    def test_can_vote_answer(self):
        """给回答投票"""
        self.answer.votes.update_or_create(user=self.user, defaults={"value": True}, )
        self.answer.votes.update_or_create(user=self.other_user, defaults={"value": True}, )
        self.answer.count_votes()
        assert self.answer.total_votes == 2  # user01与user02各投一票

    def test_get_question_voters(self):
        """问题的投票用户"""
        self.question_one.votes.update_or_create(user=self.user, defaults={"value": True}, )
        self.question_one.votes.update_or_create(user=self.other_user, defaults={"value": False})
        self.question_one.count_votes()
        assert self.user in self.question_one.get_upvoters()
        assert self.other_user in self.question_one.get_downvoters()

    def test_get_answer_voters(self):
        """回答的投票用户"""
        self.answer.votes.update_or_create(user=self.user, defaults={"value": True}, )
        self.answer.votes.update_or_create(user=self.other_user, defaults={"value": False})
        self.answer.count_votes()
        assert self.user in self.answer.get_upvoters()
        assert self.other_user in self.answer.get_downvoters()

    def test_question_str_return_value(self):
        assert isinstance(self.question_one, Question)
        assert str(self.question_one) == "问题1"

    def test_question_unanswered_question(self):
        assert self.question_one == Question.objects.get_unanswered()[0]

    def test_question_answered_question(self):
        assert self.question_two == Question.objects.get_answered()[0]

    def test_question_answers_returns(self):
        assert self.answer == self.question_two.get_answers()[0]

    def test_question_answer_count(self):
        assert self.question_two.count_answers == 1

    def test_question_accepted_answer(self):
        assert self.question_two.get_accepted_answer() == self.answer

    def test_answer_return_value(self):
        assert str(self.answer) == "问题2的正确回答"

    def test_answer_accept_method(self):
        answer_one = Answer.objects.create(
            user=self.user,
            question=self.question_one,
            content="回答1"
        )
        answer_two = Answer.objects.create(
            user=self.user,
            question=self.question_one,
            content="回答2"
        )
        answer_three = Answer.objects.create(
            user=self.user,
            question=self.question_one,
            content="回答3"
        )
        self.assertFalse(answer_one.is_answer)
        self.assertFalse(answer_two.is_answer)
        self.assertFalse(answer_three.is_answer)
        self.assertFalse(self.question_one.has_answer)
        # 接受 回答1 作为正确回答
        answer_one.accept_answer()
        self.assertTrue(answer_one.is_answer)
        self.assertFalse(answer_two.is_answer)
        self.assertFalse(answer_three.is_answer)
        self.assertTrue(self.question_one.has_answer)
        self.assertEqual(self.question_one.get_accepted_answer(), answer_one)
