from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Contact, UserMessage
from .forms import UserMessageForm
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from .models import  Message, UserMessage
from django.http import JsonResponse
from .forms import MessageForm, UserMessageForm
from django.shortcuts import render, get_object_or_404
from .forms import SearchForm
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# @login_required
# def contact_list(request):
#     contacts = Contact.objects.all()
#     return render(request, 'contact_list.html', {'contacts': contacts})
#
# @login_required
# def chat_list(request):
#     user_messages = UserMessage.objects.filter(sender=request.user)
#     return render(request, 'user_message.html', {'user_messages': user_messages})
#
# @login_required
# def chat(request, receiver_id):
#     receiver = Contact.objects.get(id=receiver_id)
#     if request.method == 'POST':
#         form = UserMessageForm(request.POST, request.FILES)
#         if form.is_valid():
#             user_message = form.save(commit=False)
#             user_message.sender = request.user
#             user_message.receiver = receiver
#             user_message.save()
#             return redirect('chat', receiver_id=receiver_id)
#     else:
#         form = UserMessageForm()
#     messages = UserMessage.objects.filter(
#         (Q(sender=request.user) & Q(receiver=receiver)) |
#         (Q(sender=receiver) & Q(receiver=request.user))
#     ).order_by('created_at')
#     return render(request, 'send_message_to_user.html', {'receiver': receiver, 'messages': messages, 'form': form})
#
#
# def home(request):
#     return render(request, 'home.html')


@login_required
def send_message_to_user(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    if request.method == 'POST':
        form = UserMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = user
            if 'attachment' in request.FILES:
                message.attachment = request.FILES['attachment']
            message.save()
            return redirect('user_messages', pk=user.id)
    else:
        form = MessageForm()
    return render(request, 'send_message_to_user.html', {'form': form, 'user': user})


class UserMessages(View):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        messages = UserMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=request.user))
        ).order_by('created_at')
        form = MessageForm()
        return render(request, 'user_messages.html', {'messages': messages, 'user': user, 'form': form})

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = user
            message.save()
            return redirect('user_messages', pk=pk)
        messages = UserMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=request.user))
        ).order_by('created_at')
        return render(request, 'user_messages.html', {'messages': messages, 'user': user, 'form': form})

# views.py
# views.py
from django.shortcuts import render
from django.contrib.auth.models import User

def home(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'home.html', context)

