from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
# from Student.models import chat,messenger


# def home(request):
# 	auth = get_object_or_404(authenticate)
# 	if request.user.is_authenticated:
# 		logout(request)
# 	return render(request,'home/home.html', {'flag':auth.login})


def register(request):
	if request.method =='POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'user/register.html', {'form': form})

@login_required
def profile(request):
	return render(request, 'user/profile.html')

def update(request):
	if request.method =='POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		prev_username = request.user.username
		if u_form.is_valid(): 
			u_form.save()
			username = u_form.cleaned_data.get('username')
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)	
	context = {
		'u_form': u_form,
	}
	return render(request, 'user/update.html', context)
