from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    # Build a dictionary of key value pairs to pass to the template engine
    context_dict = {'boldmessage': 'this variable is bold due to the HTML formatting'}

    return render(request, 'rango/index.html', context_dict)

def about(request):
    return HttpResponse("<h1>This is the about page</h1><br><br>test... test")