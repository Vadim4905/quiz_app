from django.forms.models import inlineformset_factory
from django import forms
from . import models

class NameForm(forms.Form):
    name = forms.CharField(max_length='64')
    
class CodeForm(forms.Form):
    code = forms.IntegerField()