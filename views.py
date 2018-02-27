"""from django.shortcuts import render
from django.views.generic import TemplateView"""

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout,login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from wallet.forms import RegistrationForm
#from django.contrib.auth.forms import UserCreationForm


def signup(request):
	if request.method == 'POST':
		form =RegistrationForm(request.POST)
		if form.is_valid():
			user=User.objects.create_user(
                                     username=form.cleaned_data['phone'],
                                     first_name=form.cleaned_data['username'],
                                     email=form.cleaned_data['email'],
                                     password=form.cleaned_data['password1'],
                                    )
			return HttpResponseRedirect('/wallet/login/')
	form = RegistrationForm()
	#variables = RequestContext(request, {'form': form})
	return render(request, 'signup.html', {})



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
	return render(request,'main_page.html',{})

def logout_page(request):
    logout(request)
    return redirect('/')