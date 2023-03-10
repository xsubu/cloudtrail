from django.urls import path
 
from users import views

app_name = 'appusers'

urlpatterns = [
    path('', views.register_user, name="register")
]