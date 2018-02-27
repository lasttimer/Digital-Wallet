"""from django.conf.urls import url
from wallet import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
]"""


from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

urlpatterns = patterns('',
       url(r'^login/', login ,{'template_name':'registration/login.html'}),
       url(r'^signup/', "wallet.views.signup", name='signup_url'),
       url(r'^$', "wallet.views.main_page", name='homepage'),
       url(r'^logout/',"wallet.views.logout_page", name='logout'),

)