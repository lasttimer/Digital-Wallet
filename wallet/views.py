"""from django.shortcuts import render
from django.views.generic import TemplateView"""

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.models import User
from wallet.models import balance
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
		print("hello in login")
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
			subject = 'Register'
			message = 'Thank u for registeration'
			from_email = settings.EMAIL_HOST_USER
			to_list = [user.email,]
			print(user.email)
			send_mail(subject,message,from_email,to_list,fail_silently=True)
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
	if request.method == 'POST':
		m= SendMoneyForm(request.POST, request=request or None)
		if m.is_valid():
			print("in newwww")
			r=request.POST.get('phone')
			a=request.POST.get('amount')
			sndr= balance.objects.get(username=request.user.username)
			rcvr= balance.objects.get(username=r)
			p= sndr.balance
			q= rcvr.balance
			print("rcvr balancce")
			print(q)
			data= User.objects.get(username=r)
			nam = data.first_name
			if int(p) >= int(a) and sndr.username != rcvr.username:
				p=float(p)-float(a)
				sndr.balance=p
				sndr.save()
				p=sndr.balance
				print("sndr final bal")
				print(p)
				q= rcvr.balance
				q=float(q)+float(a)
				rcvr.balance=q				
				rcvr.save()
				messages.success(request, "You have successfully sent money to " + nam + "("+r+")")	
		        #return render(request,'main_page.html',{'form':m}) 	
			else:
				messages.success(request, "Money not sent ")  
				#return render(request,'main_page.html',{'form':m})
	else:
		m=SendMoneyForm(request=request)
	return render(request, 'main_page.html', {'form': m})


	#m = SendMoneyForm(None or request.POST, request=request )
	
	"""m = SendMoneyForm(request.POST, request=request or None)
	if request.method == 'POST':
	    if m.is_valid():
	       	print("m is valid")
	       	r=request.POST.get('phone')
	       	a=request.POST.get('amount')
	       	user = User.objects.get(username=request.user.username)
	       	data =  User.objects.get(username=r)
	       	print(data.first_name)
	       	s = balance.objects.get(username=user)
	       	x = balance.objects.get(username=r)
	       	p=float(x.balance)
	       	print("p= ")
	       	print(p)
	       	q= s.balance
	       	print("q= ")
	       	print(q)
	       	nam = data.first_name
	       	if int(q)>=int(a):
	       		print("condition is true")	        	
		       	q = q-float(a)
		       	print("before balance ")
		       	print(s.balance)
		       	s.balance=q
		       	print("after balance ")
		       	print(s.balance)
		       	s.save()
		       	p = p+float(a)
		       	x.balance=p
		      	x.save()		     	
		        messages.success(request, "You have successfully sent money to " + nam + "("+r+")")	
		        return render(request,'main_page.html',{'form':m, 'data': data,}) 	    
		    else :
		    	messages.success(request, "Money not sent ")
		     		
	m=SendMoneyForm(request=request or None)
	return render(request,'main_page.html',{'form':m}) """

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
