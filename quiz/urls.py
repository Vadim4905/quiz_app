from . import views
from django.urls import path


app_name = 'quiz'
urlpatterns = [
    path('', views.QuizListView.as_view(),name='quiz-list'),
    path('<uuid:pk>', views.QuizDetailView.as_view(),name='quiz-detail'),
    
    path('create', views.QuizCreateView.as_view(),name='quiz-create'),
    path('<uuid:pk>/delete', views.QuizDeleteView.as_view(),name='quiz-delete'),
    path('<uuid:pk>/edit', views.QuizUpdateView.as_view(),name='quiz-update'),
    
    path('<uuid:quiz_pk>/question/<str:model_name>/create', views.QuestionCreateUpdateView.as_view(),name='question-create'),
    path('<uuid:quiz_pk>/question/<str:model_name>/<int:pk>', views.QuestionCreateUpdateView.as_view(),name='question-update'),
    path('question/<int:pk>/delete', views.QuestionDeleteView.as_view(),name='question-delete'),
    
    path('<int:question_id>/answer/create', views.AnswerCreateView.as_view(),name='answer-create'),
    
]
