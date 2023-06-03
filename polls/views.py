from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from.models import Question, Choice
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Get question to display them
def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:10]
    choice_list = Choice.objects.all()
    context = {
        'latest_question_list': latest_question_list,
        'choice_list': choice_list
    }
    return render(request, 'index.html', context)
#specific question and choices
def detail(request, question_id):
    choice_list = Choice.objects.all()
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question':question, 'choice_list': choice_list})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account has been created! you are now able to log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

#Get question and display results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {'question': question, 'error_message':
            "you didnt select a choice", })
    if request.method == 'POST':
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        user = request.user
        if selected_choice.voters.filter(pk=user.pk).exists():
            return render(request, 'detail.html', {'question':question,
                                                   'error_message':'you have already voted for this person'})
        else:
            selected_choice.votes +=1
            selected_choice.voters.add(user)
            selected_choice.save()
            return HttpResponseRedirect(reverse('results', args=(question.id,)))
    return HttpResponseRedirect(reverse('detail', args=(question.id,)))


def about(request, pk):
    choice = get_object_or_404(Choice, id=pk)
    context = {
        'choice': choice
    }
    return render(request, 'about.html', context)



'''
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {'question':question, 'error_message':
                                               "you didnt select a choice",})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        # This prevents the data from being posted twice if a user hits the Back button
        return HttpResponseRedirect(reverse('results', args=(question.id,)))
'''

