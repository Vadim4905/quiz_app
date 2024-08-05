from django.db import models
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser 
from django.core.validators import MaxValueValidator,MinValueValidator

import uuid
from random import randint
from .fields import UniqueRandomCode


# Create your models here.




class QuizSession(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    code = UniqueRandomCode(unique=True,validators=[MaxValueValidator(999999),MinValueValidator(100000)])
    creator = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='quiz_sessions')
    quiz = models.ForeignKey('quiz.Quiz',on_delete=models.CASCADE,related_name='quiz_sessions')
    created = models.DateTimeField(auto_now_add=True)
    
        
class SessionUser(models.Model):
    session = models.ForeignKey(QuizSession,on_delete=models.CASCADE,related_name='users')
    name = models.CharField(max_length=64)
    
    class Meta:
        unique_together = ('session','name')
        
    def __str__(self):
        return self.name
