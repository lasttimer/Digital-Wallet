"""from django.shortcuts import render
from django.views.generic import TemplateView"""

from django.shortcuts import render
from django.contrib.auth.models import User
from wallet.models import balance
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from wallet.forms import RegistrationForm, LoginForm, SendMoneyForm
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.core.exceptions import ValidationError
#from django.contrib.auth.forms import UserCreationForm



def login(request):
	l = LoginForm(request.POST or None)
	if request.method == 'POST':
		print("hello")
		#phone = request.POST.get('phone')
        #password = request.POST.get('password')
        if l.is_valid():
        	nam=request.POST.get('phone')
        	user = authenticate(username=request.POST.get('phone'), password=request.POST.get('password'))
        	#auth_login(request,user)
        	if user:
        		auth_login(request,user)
        		return HttpResponseRedirect('/')
        	else:
        		l = LoginForm()
			#error = " Sorry! Phone Number and Password didn't match, Please try again ! "
			#return render(request, 'registration/login.html',{})
		
	return render(request, 'registration/login.html', {'form': l})


def signup(request):
	if request.method == 'POST':
		f =RegistrationForm(request.POST)
		if f.is_valid():
			user=User.objects.create_user(
                                     username=f.cleaned_data['phone'],
                                     first_name=f.cleaned_data['username'],
                                     email=f.cleaned_data['email'],
                                     password=f.cleaned_data['password1'],
                                    )
			bala=balance.objects.create(username=f.cleaned_data['phone'], balance=0, fd=0,)
			bala.save()
			messages.success(request, 'Account created successfully Please Login')
			return HttpResponseRedirect('/wallet/login/')
		#else:
			#messages.warning(request, 'Please correct the error below.')
	        #return render(request, 'signup.html',{'form': f})
	        #return HttpResponseRedirect(reverse('signup_url'))"""
	else:
		f = RegistrationForm()

	return render(request, 'signup.html', {'form': f})
		#form = RegistrationForm(request.user)
	#variables = RequestContext(request, {'form': form})
		#return render(request, 'signup.html', {})# {'form': form})




"""def user_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(username=phone, password=password)
        if user:
            login(request,user)
            return HttpResponseRedirect('/users/home')
        else:
            error = " Sorry! Phone Number and Password didn't match, Please try again ! "
            return render(request, 'login.html',{'error':error})
    else:
        return render(request, 'login.html',{})"""




"""def main_page(request):
    template = get_template('main_page.html')
    variables = Context({ 'user': request.user })
    output = template.render(variables)
    return HttpResponse(output)"""
def main_page(request):
	m = SendMoneyForm(request.POST or None)
	if request.method == 'POST':
		print("hello")
        if m.is_valid():
        	r=request.POST.get('phone')
        	a=request.POST.get('amount')
        	user = User.objects.get(username=request.user.username)
        	data = balance.objects.get(username=user)
        	x = balance.objects.get(username=r)
        	p=x.balance
        	q=data.balance
        	if q>=p:
	        	
	        	p = p+float(a)
	        	x.balance=p
	        	x.save()
	        	
	        	q = q-float(a)
	        	data.balance=q
	        	data.save()     		
	return render(request,'main_page.html',{'form':m})

def addmoney(request):
	if request.method == 'POST':
		new=request.POST.get('amount')
		user = User.objects.get(username=request.user.username)
		print(user)
		data = balance.objects.get(username=user)
		print(data.balance)
		var=data.balance
		var=var+float(new)
		data.balance=var
		data.save()
	return render(request,'addmoney.html',{})

def bal(request):
	user = User.objects.get(username=request.user.username)
	print(user)
	data = balance.objects.get(username=user)
	print(data.balance)
	#b={"bala":data}
	return render(request, 'balance.html', {'data': data,})

def logout_page(request):
    logout(request)
    return redirect('/')