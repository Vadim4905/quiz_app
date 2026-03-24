import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import render,get_object_or_404,redirect
from asgiref.sync import sync_to_async
from django.http import Http404
from channels.layers import get_channel_layer
from django.template import Context, Template
from django import forms

from . import models

class AdminConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        try:
            models.QuizSession.objects.aget(models.QuizSession,id=self.session_id,creator=self.user)
        except models.QuizSession.DoesNotExist:
            raise Http404

        self.room_group_name = f'admin_{self.session_id}'
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        
        await self.accept()
        
 
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        
    async def new_user(self,event):
        await self.send(text_data=json.dumps(event))

    async def question(self,event):
        await self.send(text_data=json.dumps(event))
        
    async def disconected_user(self,event):
        await self.send(text_data=json.dumps(event))

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     self.send(text_data=json.dumps({'message': message}))
        
class ClientConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.client_id = self.scope['session'].get('quiz_session_user_id')
        try:
            self.session_user = await models.SessionUser.objects.select_related('session').aget(id=self.client_id)
        except:
            raise Http404
        self.session_id =self.session_user.session.id
        
        self.room_group_name = f'client_{self.session_id}'
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()
        

            
        
        await self.channel_layer.group_send(
                f'admin_{self.session_id}',
                {
                    "type": "new_user",
                    "message": f'New user ',
                    "username": self.session_user.name,
                }
            )


        
    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
                f'admin_{self.session_id}',
                {
                    "type": "disconected_user",
                    "message": f'disconected user',
                    "username": self.session_user.name,
                }
            )
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
    
    async def new_user(self,event):
        await self.send(text_data=json.dumps(event))
        
    async def question(self,event):
        await self.send(text_data=json.dumps(event))
#         form = type('form', (forms.Form,), atr)
#         template = Template("""<form action="" method="post" enctype="multipart/form-data">
#     {{ form.as_p }}
#     {% csrf_token %}
#     <button type="submit" class="small-gray-btn">{% translate "submit" %} </button>
# </form>""")
#         context = Context({"message":'message'})
#         rendered_question = template.render(context)
        
#         await self.send(
#             text_data=json.dumps(
#                 {
#                 'type':'question',
#                 'question':rendered_question
#                 }
#                 )
#             )
        
    async def disconected_user(self,event):
        await self.send(text_data=json.dumps(event))

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     self.send(text_data=json.dumps({'message': message}))