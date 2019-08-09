from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):


	phone = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Phone number'}))
	password1 = forms.CharField(label='', widget=forms.PasswordInput(
		attrs={'placeholder':'Password'}),
	)

	password2 = forms.CharField(label='', widget=forms.PasswordInput(
		attrs={'placeholder':'Password confirmation'}))


	class Meta(UserCreationForm):
		model = CustomUser
		fields = ['username','email']
		labels = {'username':'', 'email':''}
		help_texts = {'username':''}
		widgets = {'username':forms.TextInput(attrs={'placeholder':'Username'}),
        'email':forms.EmailInput(attrs={'placeholder':'Email address'})}

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username','email')
