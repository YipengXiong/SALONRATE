from django.shortcuts import render
from salonrate.models import UserProfile
from salonrate.forms import UserForm, UserProfileForm
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
def register(request):
    # Set a boolean value to indicate the registration state.
    registered = False

    # If receiving a 'POST' request, register
    if request.method == 'POST':
        # Acquire information entered by the user
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If two forms are valid, register this user
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            # If user upload a picture for avatar, get it from the request
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            # Save profile
            profile.save()
            # Set registered to True
            registered = True
        else:
            # If two forms are invalid, print the errors
            print(user_form.errors, profile_form.errors)
    
    else:
        # If not a POST request, simply show the forms
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, 'salonrate/register.html', context=context_dict)

def user_login(request):
    # If receiving a 'POST' request, check whether the user can log in 
    if request.method=='POST':
        # Acquire the messages entered by the user
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check whether this user is authenticated
        user = authenticate(username=username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('salonrate:homepage'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        # If not a POST request, go to the login page
        return render(request, 'salonrate/login.html')