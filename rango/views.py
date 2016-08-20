from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfile

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. of likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5] # the '-' in front of 'likes' means DESCENDING order

    # Build a dictionary of key value pairs to pass to the template engine
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    return render(request, 'rango/index.html', context_dict)

def about(request):
    message = "<a href='/rango/'>Index</a><br><br><h1>This is the about page</h1><br><br>test... test"
    return HttpResponse(message)

def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {'category_name_slug': category_name_slug}

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

def add_category(request):
    # a HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # is this a valid form?
        if form.is_valid():
            form.save(commit=True)

            #send the user back to the index page
            return index(request)

        else:
            # if the form isn't valid, display the errors
            print form.errors

    else:
        # if it wasn't a POST request, show the form to the user
        form = CategoryForm()

    # If the form (or the form details) is bad or no form supplied
    # Render the form with any error messages
    return render(request, 'rango/add_category.html', {'form':form})

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category':cat,'category_name_slug':category_name_slug}

    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    # Default value for registration validation
    registered = False

    # If this is a POST, we need to process the form data
    if request.method == 'POST'
        # Try to get the form info and apply to both UserForm AND UserProfile
        user_form = UserForm(data=request.POST)
        profile_form = UserProfile(data=request.POST)

        # If both forms are valid...
        if user_form.is_valid() and user_profile.is_valid():

            # Save the UserForm data to the database
            user = user_form.save()
            # Hash their password
            user.set_password(user.password)
            # Update the hashed password
            user.save()

            # Now sort out the UserProfile instance:
            # Delay saving the model until we set the user attribute
            # by setting commit=False. This avoids data integrity issues
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did they provide a photo? If so, get it from the form and put in UserProfile
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # NOW save the UserProfile...
            profile.save()

            # ...and update our registration status
            registered = True

        # Invalid form or mistakes? Print to terminal and show the user
        else:
            print user_form.errors, user_profile.errors

    # Not a HTTP POST, so we render our blank form with the two model instances
    else:
        user_form = UserForm()
        profile_form = UserProfile()

    # Return the template depending on the context
    return render(request,
                  'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
                  )

def user_login(request):
    # If it's a POST, get the relevant info
    if request.method == 'POST':
        # Collect username and pw provided from login form
            # Use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
            # because the request.POST.get('<variable>') returns None, if the value does not exist,
            # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's processes to determin if the credentials are valid
        # and return a User object if so
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Make sure the acct isn't disabled
            if user.is_active:
                # If it's valid and active, send them to Homepage
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # Valid but inactive account
                return HttpResponse("Your account has been disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login credentials supplied.")
    # The request is not POST, so display the form
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return  render(request, 'rango/login.html/', {})