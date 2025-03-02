from django.shortcuts import render
from stripe_test.settings import BASE_DIR


def index(request):
    return render(request, 'index.html')


def sucsess(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')
