"""from django.conf.urls import url
from wallet import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
]"""


from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
       url(r'^login/', "wallet.views.login" ,name='login_url'),
       url(r'^signup/', "wallet.views.signup", name='signup_url'),
       url(r'^$', "wallet.views.main_page", name='homepage'),
       url(r'^addmoney/', "wallet.views.addmoney", name='addmoney'),
       url(r'^balance/', "wallet.views.bal", name='balance'),
       url(r'^logout/',"wallet.views.logout_page", name='logout'),

)  