from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.urls import reverse

import uuid

# Create your models here.






class Quiz(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='quizzes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
        'quiz:quiz-detail',
        args=[self.id]
        )
    



class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='questions')
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': ('textquestion', 'optionquestion','booleanquestion' )
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['created']
        

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    title = models.CharField(max_length=255) 
    
    def __str__(self):
        return self.title
    class Meta:
        unique_together = ('question','title')
    
class QuestionBase(models.Model):
    image = models.ImageField(upload_to='images',null=True,blank=True)
    time_limit = models.IntegerField(default=30)
    title = models.CharField(max_length=255) 
    
    def __str__(self):
        return self.title    
     
    class Meta:
        abstract = True
       
    
    
class TextQuestion(QuestionBase):
    pass
    
    
class BooleanQuestion(QuestionBase):
    pass


class OptionQuestion(QuestionBase):
    pass
    


class Option(models.Model):
    question = models.ForeignKey(OptionQuestion,on_delete=models.CASCADE,related_name='options')
    title = models.CharField(max_length=255) 
    
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['question']
    

 