from django import forms

# creating a form
class ResetPasswordForm(forms.Form):
	password = forms.CharField(max_length = 200)
	password2 = forms.CharField(max_length = 200)
	