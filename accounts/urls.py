from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [    
    path('signup/', SignUp.as_view(), name='user_signup'),
    path('login/', Login.as_view(), name='user_login'),
    path('logout/', user_logout, name='user_logout'),
]