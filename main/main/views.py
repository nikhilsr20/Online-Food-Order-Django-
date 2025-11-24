from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect

def redir(request): 
    return redirect('home')