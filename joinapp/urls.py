from django.urls import path 
from . import views 
urlpatterns=[
    path('joinus',views.joinus,name='joinus'),
    path('login',views.login,name="login"),
    
]