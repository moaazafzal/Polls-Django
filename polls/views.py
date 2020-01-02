from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Question, Choice
from django.shortcuts import render
from django.views import generic,View
from django.utils import timezone
from polls.form import QuestionForm, ChoiceForm,ContactForm



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class DetailFormClass(generic.FormView):
    template_name = "polls/details.html"

    def get(self, request, *args, **kwargs):
        myquestion=Question.objects.get(id=kwargs['pk'])
        # choice_form = ChoiceForm()
        # question_form=QuestionForm()
        #
        #
        context = {"question" :myquestion}
        return render(request, self.template_name,context)

    def post(self, request, *args, **kwargs):
        question = get_object_or_404(Question, id=kwargs['pk'])
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))





class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print(request.POST['choice']+"  hhhhh")
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class VoteView(View):
    template_name = 'polls/detail.html'

    def get(self, request):

        obj = get_object_or_404(Question, pk=id)
        print("hrhr")
        return render(request, 'polls/detail.html', {
            'question': obj,
            'error_message': "You didn't select a choice.",
        })

    def post(self, request, id =None, *args, **kwargs):

        if 'question.id' is request.POST:
            print('haha')

        print(" MyPost "+request.POST.get('choice'))
        obj = get_object_or_404(Question, pk=id)
        try:
            selected_choice = obj.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': obj,
                'error_message': "You didn't select a choice.",
            })
        # else:
        #     selected_choice.votes += 1
        #     selected_choice.save()
        #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


        # question = get_object_or_404(Question, pk=id)
        # try:
        #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # except (KeyError, Choice.DoesNotExist):
        #     return render(request, 'polls/detail.html', {
        #         'question': question,
        #         'error_message': "You didn't select a choice.",
        #     })
        # else:
        #     selected_choice.votes += 1
        #     selected_choice.save()
        #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))




# class MyVoteView(View):
#     def get(self,request, slug):
#         question = get_object_or_404(Question, pk=slug)
#         return render(request, 'polls/detail.html', question)
#     def post(self,request):
#
#         form =ChoiceForm(request.POST)
#         if form.is_valid():
#             choice=form.save()
#             return HttpResponseRedirect(reverse('polls:results', args=(slug,)))


def Question_create_view(request):
    form=QuestionForm(request.POST or None)
    if form.is_valid():
        form.save()

    form1 = ChoiceForm(request.POST or None)
    if form1.is_valid():
        form1.save()

    context = {
        'form': form, 'form1': form1
    }
    return render(request, 'polls/form.html', context)


class ContactView(generic.FormView):
    template_name = 'polls/form.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)