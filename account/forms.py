from django import forms 

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


class EmailPostForm(forms.Form):
	to = forms.EmailField()
	to.clean('email@example.com')