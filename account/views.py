from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .forms import LoginForm, EmailPostForm, UserRegistrationForm, \
				   UserEditForm, ProfileEditForm
from .models import Profile


# Create your views here.

def user_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request,
								username=cd['username'],
								password=cd['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponse('Authenticated successfully')
			else:
				return HttpResponse('Disabled account')
		else:
			return HttpResponse('Invalid login')
	else:
		form = LoginForm()
	return render(request, 'account/login.html', {'form': form})


@login_required      # Наш обработчик обернут в декоратор login_required. Он проверяет, авторизован ли пользователь. Если пользователь авторизован, Django выполняет обработку. В противном случае пользователь перенаправляется на страницу логина. При этом в GET-параметре задается next -адрес запрашиваемой страницы. Таким образом, после успешного прохождения авторизации пользователь будет перенаправлен на страницу, куда он пытался попасть. Именно для этих целей мы вставили скрытое поле next в форму логина.
def dashboard(request):
	return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def reset_password_to_email(request):
	sent=False
	if request.method == 'POST':
		# the form was sent for safe
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# all the forms passed validation
			cd = form.cleaned_data
			# ... sending email
			send_mail('admin@myblog.com', [cd['to']])
			sent=True
	else:
		form = EmailPostForm()
	return render(request, 'account/registration/password_reset_done.html')


def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			# create new user, but don`t save it to DB
			new_user = user_form.save(commit=False)
			# add user encrypted password
			new_user.set_password(user_form.cleaned_data['password'])
			# save user in DB
			new_user.save()
			# create user profile 
			Profile.objects.create(user=new_user)
			return render(request, 'account/register_done.html', {'new_user': new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user,data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile,
									   data=request.POST,
									   files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Profile updated successfully')
		else:
			messages.error(request, 'Error updating your profile')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)
	return render(request,'account/edit.html',{'user_form': user_form, 'profile_form': profile_form})
