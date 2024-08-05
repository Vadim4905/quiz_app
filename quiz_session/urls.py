from . import views
from django.urls import path


app_name = 'quiz_session'


urlpatterns = [
    path('<uuid:quiz_pk>/create_session', views.CreateQuizSessionView.as_view(),name='create-session'),
    path('host_live/<uuid:session_pk>', views.AdminSessionView.as_view(),name='admin-view-session'),
    path('join', views.JoinSessionView.as_view(),name='join-session'),
    path('complete', views.ClientSessionView.as_view(),name='client-view-session'),
]
