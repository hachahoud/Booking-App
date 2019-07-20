from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
	"""Register a new user."""
	if request.method != 'POST':
		form = CustomUserCreationForm()
	else:
		form = CustomUserCreationForm(data=request.POST)
		if form.is_valid():
			new_user = form.save()
			authenticated_user = authenticate(username=new_user.username,
				password=request.POST['password1'])
			login(request, authenticated_user)
			return HttpResponseRedirect(reverse("bookings:date"))

	context = {'form':form}
	return render(request, 'users/register.html',context)

@login_required
def logout_view(request):
	"""Log the user out."""
	logout(request)
	return HttpResponseRedirect(reverse("bookings:home"))