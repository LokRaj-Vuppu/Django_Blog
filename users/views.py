from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, userUpdateForm, profileUpdateForm
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created. You can Login now!')
			return redirect('login')
	else:
		form = UserRegistrationForm()
	return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
	if request.method == 'POST':
		user_form = userUpdateForm(request.POST, instance=request.user)
		profile_form = profileUpdateForm(request.POST, request.FILES,
													 instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid:
			user_form.save()
			profile_form.save()
			messages.success(request, f'Your account has been updated')
			return redirect('profile')
	else:
		user_form = userUpdateForm(instance=request.user)
		profile_form = profileUpdateForm(instance=request.user.profile)
		
	context = {
		'user_form': user_form,
		'profile_form': profile_form
	}
	return render(request, 'users/profile.html', context)