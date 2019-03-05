#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView, DetailView

from zanhu.helpers import ajax_required
from zanhu.qa.models import Question, Answer
from zanhu.qa.forms import QuestionForm
from zanhu.notifications.views import notification_handler


class QuestionsListView(LoginRequiredMixin, ListView):
    """所有问题"""
    model = Question
    paginate_by = 20
    context_object_name = "questions"
    template_name = "qa/question_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["popular_tags"] = Question.objects.get_counted_tags()  # 页面的标签功能
        context["active"] = "all"
        return context


class AnsweredQuestionsListView(QuestionsListView):
    """已回答的问题，继承自QuestionsListView"""

    def get_queryset(self, **kwargs):
        return Question.objects.get_answered()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["active"] = "answered"
        return context


class UnansweredQuestionsListView(QuestionsListView):
    """未回答的问题，继承自QuestionsListView"""

    def get_queryset(self, **kwargs):
        return Question.objects.get_unanswered()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["active"] = "unanswered"
        return context


class QuestionDetailView(LoginRequiredMixin, DetailView):
    """问题详情"""
    model = Question
    context_object_name = "question"
    template_name = 'qa/question_detail.html'


class CreateQuestionView(LoginRequiredMixin, CreateView):
    """提出问题"""
    form_class = QuestionForm
    template_name = "qa/question_form.html"
    message = "问题已提交！"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("qa:unanswered_q")

    """
    用如下方式改写form_valid()
    @method_decorator(login_required, name='dispatch')
    class PostUpdateView(UpdateView):
        model = Post
        fields = ('message',)
        template_name = 'boards/edit_post.html'
        pk_url_kwarg = 'post_pk'
        context_object_name = 'post'
    
        def get_queryset(self):
            queryset = super().get_queryset()
            return queryset.filter(created_by=self.request.user)
    
        def form_valid(self, form):
            post = form.save(commit=False)
            post.updated_by = self.request.user
            post.save()
            return redirect('post_topic', pk=post.topic.board.pk, topic_pk=post.topic.pk)
    """


class CreateAnswerView(LoginRequiredMixin, CreateView):
    """回答问题"""
    model = Answer
    fields = ["content", ]
    message = "您的回答已提交"
    template_name = 'qa/answer_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs["question_id"]
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("qa:question_detail", kwargs={"pk": self.kwargs["question_id"]})


@login_required
@ajax_required
@require_http_methods(["POST"])
def question_vote(request):
    """给问题投票，AJAX POST请求"""
    question_id = request.POST["question"]
    value = True if request.POST["value"] == 'U' else False  # 'U'表示赞，'D'表示踩
    question = Question.objects.get(pk=question_id)
    users = question.votes.values_list('user', flat=True)  # 当前问题的所有投票用户

    if request.user.pk in users and (question.votes.get(user=request.user).value == value):
        question.votes.get(user=request.user).delete()
    else:
        question.votes.update_or_create(user=request.user, defaults={"value": value})

    """
    # 用户首次操作，点赞/点踩
    if request.user.pk not in users:
        question.votes.update_or_create(user=request.user, defaults={"value": value})

    # 用户已近赞过，要取消赞/踩一下
    elif question.votes.get(user=request.user).value:
        if value:
            question.votes.get(user=request.user).delete()
        else:
            question.votes.update_or_create(user=request.user, defaults={"value": value})
    # 用户已踩过，取消踩/赞一下
    else:
        if not value:
            question.votes.get(user=request.user).delete()
        else:
            question.votes.update_or_create(user=request.user, defaults={"value": value})
    """

    return JsonResponse({"votes": question.total_votes()})


@login_required
@ajax_required
@require_http_methods(["POST"])
def answer_vote(request):
    """给回答投票，AJAX POST请求"""
    answer_id = request.POST["answer"]
    value = True if request.POST["value"] == 'U' else False  # 'U'表示赞，'D'表示踩
    answer = Answer.objects.get(uuid_id=answer_id)
    users = answer.votes.values_list('user', flat=True)  # 当前回答的所有投票用户

    if request.user.pk in users and (answer.votes.get(user=request.user).value == value):
        answer.votes.get(user=request.user).delete()
    else:
        answer.votes.update_or_create(user=request.user, defaults={"value": value})

    return JsonResponse({"votes": answer.total_votes()})


@login_required
@ajax_required
@require_http_methods(["POST"])
def accept_answer(request):
    """
    接受回答，AJAX POST请求
    已近被接受的回答用户不能取消
    """
    answer_id = request.POST["answer"]
    answer = Answer.objects.get(uuid_id=answer_id)
    # 如果当前登录用户不是提问者，排除权限拒绝错误
    if answer.question.user.username != request.user.username:
        raise PermissionDenied
    answer.accept_answer()
    # 通知回答者
    notification_handler(request.user, answer.user, 'W', answer)
    return JsonResponse({'status': 'true'}, status=200)
