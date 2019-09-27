import authapp.views as authapp
from django.urls import re_path

app_name = 'authapp'


urlpatterns = [
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='verify'),
    ]