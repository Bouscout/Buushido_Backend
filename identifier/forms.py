from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

#forms to sign up a new user, but we will probably use another solution since this is server side rendering
class formulaire_incription(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields =('username',)
   
#form to login an user
class formulaire_connection(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
