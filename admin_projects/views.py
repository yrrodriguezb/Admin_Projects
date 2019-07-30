from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def _404(request, exception):
    return render(request, '_404.html')