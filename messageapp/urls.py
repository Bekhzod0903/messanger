from django.urls import path
from .views import home, send_message_view, send_message_users, UserMessages, about_site

urlpatterns = [
    path('', home, name='home'),
    path('message/', send_message_view, name='message'),
    path('message/<int:pk>/', send_message_users, name='user'),
    path('message/<int:pk>/user/', UserMessages.as_view(), name='user_messages'),
    path('about-site/', about_site, name='about-site'),  # corrected URL pattern for about_site
]
