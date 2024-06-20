from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
# from .models import  Message

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'image', 'email', 'username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('image', 'first_name', 'last_name', 'email', 'username')




#
# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email']
#
#
#
#
#
#
# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ['content']