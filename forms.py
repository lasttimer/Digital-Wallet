import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from django.utils.translation import ugettext_lazy as _
 
class RegistrationForm(forms.ModelForm): 
    username = forms.CharField(label='Username', required=True, max_length=50)
    phone = forms.CharField(label='Phone', required=True, max_length=25)
    email = forms.EmailField(label="Email", required=True, max_length=30)
    password1 = forms.CharField(required=True, max_length=30, label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, max_length=30, label="Password(Again)", widget=forms.PasswordInput())

    def clean_password2(self):
        #if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Password don't match")
            return password2
 
   
    class Meta:
        model = User
        fields = ['username','phone','email','password1','password2',]
    """def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.Validat"""