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

import random

from . import forms
from . import models
from quiz import models as quiz_models


class CreateQuizSessionView(LoginRequiredMixin,View):
    def post(self,request,quiz_pk):
        quiz = get_object_or_404(quiz_models.Quiz,pk=quiz_pk)
        session = models.QuizSession.objects.create(
            creator = request.user,
            quiz=quiz,
        )
        return redirect('quiz_session:admin-view-session',session.pk)
        
class AdminSessionView(View):
    def get(self,request,session_pk):
        session = get_object_or_404(models.QuizSession,pk=session_pk)
        return render(request,'quiz_session/lobby.html',{'session':session})
    
class JoinSessionView(TemplateResponseMixin,View):
    session = None
    template_name = 'quiz_session/join.html'
    
    def get(self,request,):
        if self.session:
            return self.render_to_response(
            {'form': forms.NameForm(), }
        )
        else:
            return self.render_to_response(
            {'form': forms.CodeForm(), }
        )
    
    def dispatch(self,request):
        code = request.GET.get('code','')
        if code :
            self.session = get_object_or_404(models.QuizSession,code=code)
        return super().dispatch(request)
    
    def post(self,request):
        if self.session:
            form = forms.NameForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                try:
                    user = models.SessionUser.objects.create(session=self.session,name=name)
                except IntegrityError:
                    form.add_error('name','This name is already taken')
                    return self.render_to_response(
                    {'form':form, }
                )
                request.session['quiz_session_user_id'] =user.pk
                return redirect('quiz_session:client-view-session')
        else:
            form = forms.CodeForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data['code']
                return redirect(reverse('quiz_session:join-session')+'?code='+str(code))
        return self.render_to_response(
                    {'form':form, }
                )
          
class ClientSessionView(View):
    def get(self,request):
        user_id = request.session.get('quiz_session_user_id')
        if not user_id:
            return redirect('quiz_session:join-session')
        try:
            self.session = models.SessionUser.objects.get(id=user_id).session
        except models.SessionUser.DoesNotExist:
            return redirect('quiz_session:join-session')
        return render(request,'quiz_session/client.html')
