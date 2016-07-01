from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5] # the '-' in front of 'likes' means DESCENDING order

    # Build a dictionary of key value pairs to pass to the template engine
    context_dict = {'categories': category_list}

    return render(request, 'rango/index.html', context_dict)

def about(request):
    return HttpResponse("<h1>This is the about page</h1><br><br>test... test")

def category(request, category_name_slug):
    try:
        context_dict = {}
        # See if name slug exists, otherwise raise DoesNotExist exception
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all assoc. pages
        # NOTE: filter returns >= 1 model instance
        pages = Page.objects.filter(category=category)

        # Add results to template context
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # If category isn't found, do nothing (the template already has a "missing category" if/else
        pass

    # Go render the page and pass it to the client
    return render(request, 'rango/category.html', context_dict)