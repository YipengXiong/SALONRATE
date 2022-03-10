from django.shortcuts import get_object_or_404, render
from salonrate.models import UserProfile, Salon, Service, Comment, Follows
from salonrate.forms import CommentForm, UserForm, UserProfileForm
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
    if request.method == 'POST':
        # Acquire the messages entered by the user
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check whether this user is authenticated
        user = authenticate(username=username, password=password)
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


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('salonrate:homepage'))


def homepage(request):
    return render(request, 'salonrate/homepage.html')


def salon_detail(request):
    return render(request, 'salonrate/salon.html')


def service_detail(request):
    service = get_object_or_404(Service, service_id=100)
    context_dict = {"service":service,"comments":None}
    comments = Comment.objects.filter(salon_or_service_id=service.service_id, type=1).order_by("-comment_id")
    if comments:
        context_dict["comments"] = comments
        context_dict["comment_count"] = len(comments)
    else:
        print("No Comments")
    
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.username = request.user
            comment.salon_or_service_id = service.service_id
            comment.type = 1
            comment.save()
            return redirect(reverse('salonrate:service'))
            # return redirect(reverse('salonrate:service', kwargs={'service_name_slug':service_name_slug}))
        else:
            print(form.errors)
    context_dict['form'] = form
    return render(request, 'salonrate/service.html', context_dict)


def search(request):
    return render(request, 'salonrate/search_result.html')

# def jsonEncoder(data):
#     json_data = []
#     for p in data:
#         print(p.__dict__)
#         p.__dict__.pop("_state") # Remove '_state'
#         json_data.append(p.__dict__) 
#     return json_data