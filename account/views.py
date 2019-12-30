from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, EmailPostForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


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
