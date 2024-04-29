
from django.contrib import admin
from django.urls import path
from account.views.google import GoogleView


urlpatterns = [
    path('login_with_google/', GoogleView.as_view(), name='google'), 
]