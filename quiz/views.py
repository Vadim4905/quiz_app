from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,View,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.base import TemplateResponseMixin
from django.forms.models import modelform_factory
from django.apps import apps
from django.http import Http404,HttpResponseRedirect,HttpResponse
from django import forms
from django.forms import formsets
from django.urls import reverse_lazy,reverse
from django.db.utils import IntegrityError
from django.contrib import messages
from django.db.utils import IntegrityError

import random

from .forms import OptionFormSet
from . import models

# Create your views here.

class QuizListView(ListView):
    model = models.Quiz
    context_object_name = 'quizzes'
    template_name ='quiz/quiz_list.html'
    
class QuizDetailView(DetailView):
    model = models.Quiz
    context_object_name = 'quiz'
    
class QuizUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Quiz
    fields = ['title']
    template_name = 'quiz/quiz_form.html'
    
class QuizCreateView(LoginRequiredMixin,CreateView):
    model = models.Quiz
    fields = ['title']
    template_name = 'quiz/quiz_form.html'
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return super().form_valid(form)
    
class QuizDeleteView(LoginRequiredMixin,DeleteView):
    model = models.Quiz
    template_name = 'quiz/quiz_confirm_delete.html'
    success_url = reverse_lazy('quiz:quiz-list')

    
    
    
class QuestionCreateUpdateView(TemplateResponseMixin,View):
    template_name = 'quiz/question_form.html'
    obj = None
    model = None
    
    def get_model(self, model_name):
        if model_name in ['textquestion', 'optionquestion','booleanquestion']:
            return apps.get_model(
                app_label='quiz', model_name=model_name
            )
        raise Http404
    
    def dispatch(self,request,quiz_pk,model_name,pk=None):
        self.quiz = get_object_or_404(
            models.Quiz, pk=quiz_pk
            )
        self.model = self.get_model(model_name)
        if pk :
            self.obj = get_object_or_404(
                self.model, pk=pk
                )
        
        return super().dispatch(request,quiz_pk,model_name,pk)
    
    def get_form(self, model, *args, **kwargs):
        
        Form = modelform_factory(
            model, fields=['title','time_limit','image'])
        return Form(*args, **kwargs)

    def get(self,request,quiz_pk,model_name,pk=None):

        formset = None
        if self.model == models.OptionQuestion :
            formset = OptionFormSet(instance=self.obj)
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {'form': form, 'object': self.obj,'formset':formset}
        )
    
    def post(self,request,quiz_pk,model_name,pk=None):
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES,
        )

        if form.is_valid() :
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            if not pk:
                models.Question.objects.create(quiz=self.quiz, item=obj)
            if self.model == models.OptionQuestion:
                formset = OptionFormSet(request.POST,instance=obj)
                if not formset.is_valid() :
                    return self.render_to_response(
                {'form': form, 'object': self.obj}
                )
                formset.save()
            return redirect('quiz:quiz-detail', self.quiz.pk)
        return self.render_to_response(
                    {'form': form, 'object': self.obj}
                )

class QuestionDeleteView(View):
    
    def post(self,request,pk):
        question = get_object_or_404(models.Question,id=pk)
        question.item.delete()
        question.delete()
        return redirect('quiz:quiz-detail',question.quiz.pk)
    
class AnswerCreateView(View):
    def post(self,request,question_id):
        question = get_object_or_404(models.Question,id=question_id)
        answer = request.POST.get('answer')
        if answer:
            try:
                models.Answer.objects.create(question=question,title=answer)
            except IntegrityError:
                messages.error(request, "This answer already exist")
        return redirect('quiz:quiz-detail',question.quiz.pk)
        


            
        