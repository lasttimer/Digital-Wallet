import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,get_user_model, login, logout
from wallet.models import balance
#from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    phone = forms.CharField(label='',required=True, min_length=10, max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Mobile No.'}))
    password = forms.CharField(label='', required=True, max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self, *args, **kwargs):
        phone = self.cleaned_data['phone']
        password = self.cleaned_data['password']
        if phone and password:
            user = authenticate(username=phone, password=password)
            if not user:
                raise ValidationError("Please enter a valid Mobile no. and password!")
            #if not user.check_password(user.password):
                #raise ValidationError("Invalid password")
        return super(LoginForm, self).clean(*args, **kwargs)

 
class RegistrationForm(forms.Form): 
    username = forms.CharField(label='', required=True, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    phone = forms.CharField(label='', required=True, min_length=10, max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Mobile No.'}))
    email = forms.EmailField(label='', required=True, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(required=True, max_length=30, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, max_length=30, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
       
    class Meta:
        model = User
        fields = ['username','phone','email','password1','password2',]

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email
    
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise ValidationError('Passwords do not match.')

    def clean_phone(self):
        username = self.cleaned_data['phone']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('The mobile number you entered already exists with another account.')


    """def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("All is well")

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        print(password2)
        if password1 != password2:
            print("in the loop")
            raise forms.ValidationError(
                "Password do not match")
        return password2"""
    """def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))"""


class SendMoneyForm(forms.Form):
    phone = forms.CharField(label='',required=True, min_length=10, max_length=10,  widget=forms.TextInput(attrs={'placeholder': 'Mobile No.'}))
    amount = forms.FloatField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Amount'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request' or None)
        super(SendMoneyForm, self).__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.search(r'^\w+$', phone):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=phone)
        except User.DoesNotExist:
            raise forms.ValidationError('MObile number is NOT Registered')
        return phone

    def clean_amount(self):
        if 'phone' in self.cleaned_data:
            phone = self.cleaned_data['phone']
            amount = int(self.cleaned_data['amount'])
            usr = self.request.user.username
            data = balance.objects.get(username=usr)
            var=data.balance
            print (var)
            print (amount)
            if amount>var:
                raise  ValidationError("You have Insufficient Balance for this transaction please check your balance and retry")
            elif amount<=0:
                raise ValidationError("Please Enter a valid amount")
            return amount

    """def clean_amount(self):
        amt = self.cleaned_data['amount']
        user = User.objects.get(username=request.user.username)
        data = balance.objects.get(username=user)
        if amt<data.balance:
            raise forms.ValidationError("Insufficient Balance")
        return amt"""
