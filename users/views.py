from django.contrib.auth import login,logout
from django.shortcuts import render
from django.views import  View
from django.shortcuts import render, redirect
from .forms import CustomUserForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserForm, ProfileUpdateForm
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views import View
# from django.contrib.auth.models import User
# from .forms import  UserUpdateForm, ProfileUpdateForm, MessageForm
# from .models import Notification, Message
# from django.http import JsonResponse


# Create your views here.

class RegisterView(View):
    def get(self, request):
        create_form = CustomUserForm()
        context = {
            'form': create_form
        }
        return render(request, 'register.html', context=context)

    def post(self, request):
        create_form = CustomUserForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                'form': create_form
            }
            return render(request, 'register.html', context=context)

        # username = request.POST['username']
        # email = request.POST['email']
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        # password = request.POST['password']
        #
        # user = CustomUser.objects.create_user(
        #     username=username,
        #     email=email,
        #     first_name=first_name,
        #     last_name=last_name,
        # )
        # user.set_password(password)
        # user.save()

class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            'form': login_form
        }
        return render(request, 'login.html', context=context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
        else:
            context = {
                'form': login_form
            }
            return render(request, 'login.html', context=context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class LogoutViews(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        return redirect('home')



class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html', {"user": request.user})


class ProfileUpdateView(View):
    def get(self, request):
        update_form = ProfileUpdateForm(instance=request.user)
        return render(request, 'profile_update.html', {"form": update_form})

    def post(self, request):
        update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('users:profile')
        else:
            return render(request, 'profile_update.html', {"form": update_form})

# @login_required
# def welcome(request):
#     return render(request, 'users/welcome.html', {'username': request.user.username})
#
#
# @login_required
# def upload_painting(request):
#     if request.method == 'POST':
#         form = PaintingForm(request.POST, request.FILES)
#         if form.is_valid():
#             painting = form.save(commit=False)
#             painting.user = request.user
#             painting.save()
#             return redirect('users:my_paintings')
#     else:
#         form = PaintingForm()
#     return render(request, 'users/upload_painting.html', {'form': form})
#
#
#
# # class UserProfileView(View):
# #     def get(self, request, pk):
# #         user = get_object_or_404(User, pk=pk)
# #         return render(request, 'users/profile.html', {'profile_user': user})
#
#
# @login_required
# def profile(request, pk):
#     profile_user = get_object_or_404(User, pk=pk)
#     if not hasattr(profile_user, 'profile'):
#         Profile.objects.create(user=profile_user)
#
#     if request.method == "POST":
#         if request.user != profile_user:
#             return HttpResponseForbidden("You are not allowed to edit this profile.")
#
#         u_form = UserUpdateForm(request.POST, instance=profile_user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             return redirect('users:profile', pk=profile_user.pk)
#     else:
#         u_form = UserUpdateForm(instance=profile_user)
#         p_form = ProfileUpdateForm(instance=profile_user.profile)
#
#     context = {
#         'u_form': u_form,
#         'p_form': p_form,
#         'profile_user': profile_user
#     }
#
#     return render(request, 'users/profile.html', context)
#
#
# @login_required
# def inbox(request):
#     user_chats = Message.objects.filter(recipient=request.user).values('sender').distinct()
#     chat_messages = {}
#     for chat in user_chats:
#         sender_id = chat['sender']
#         sender = User.objects.get(id=sender_id)
#         messages = Message.objects.filter(sender=sender, recipient=request.user)
#         chat_messages[sender] = messages
#
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             recipient = User.objects.get(username=request.POST.get('recipient_username'))
#             message.recipient = recipient
#             message.save()
#             Notification.objects.create(user=message.recipient, message=f'New message from {message.sender.username}')
#             return JsonResponse({'status': 'success', 'message': message.content, 'sender': message.sender.username})
#         else:
#             return JsonResponse({'status': 'error', 'errors': form.errors})
#
#     form = MessageForm()
#     return render(request, 'users/inbox.html', {'chat_messages': chat_messages, 'form': form})
#
#
#
# @login_required
# def send_message(request, recipient_username):
#     recipient = get_object_or_404(User, username=recipient_username)
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.recipient = recipient
#             message.save()
#             Notification.objects.create(user=message.recipient, message=f'New message from {message.sender.username}')
#             return redirect('users:inbox')
#     else:
#         form = MessageForm()
#     return render(request, 'users/send_message.html', {'form': form, 'recipient_username': recipient_username})
#
# @login_required
# def notifications(request):
#     notifications = Notification.objects.filter(user=request.user, read=False)
#     return render(request, 'users/notifications.html', {'notifications': notifications})