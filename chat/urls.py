from django.urls import path
from .views import  send_message_to_user, UserMessages

app_name = 'chat'

urlpatterns = [
    path('message/<int:pk>/', send_message_to_user, name='user'),
    path('message/<int:pk>/user/', UserMessages.as_view(), name='user_messages'),
    # path('group/<int:pk>/send/', SendMessageView.as_view(), name='send_message'),
]