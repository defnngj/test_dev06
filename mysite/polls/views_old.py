from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Question, Choice
from django.http import Http404
from django.urls import reverse


def index(request):
    """问题列表"""
    print("aaaa")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'question_list': latest_question_list}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    """问题的详情页面"""
    print("问题的id", question_id)
    q = get_object_or_404(Question, pk=question_id)
    # try:
    #     q = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("问题id不存在")
    # print(q.question_text)

    # c1 = Choice.objects.filter(question=q)
    # c2 = Choice.objects.filter(question_id=q.id)
    # for c in c2:
    #     print(c.choice_text)

    return render(request, 'polls/detail.html', {'question': q})


def results(request, question_id):
    """投票的结果页面"""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    """计算投票动作"""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))












