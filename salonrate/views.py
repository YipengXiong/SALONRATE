import json
from django.shortcuts import get_object_or_404, render
from salonrate.models import UserProfile, Salon, Service, Comment, Follows
from django.core import serializers
from salonrate.forms import CommentForm, UserForm, UserProfileForm
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q


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


def salon_detail(request, salon_name_slug="rich-hair-beauty-salon"):
    return render(request, 'salonrate/salon.html')


def service_detail(request, service_name_slug="eyebrows-eyelashes-191"):
    service = get_object_or_404(Service, slug=service_name_slug)
    context_dict = {"service": service, "comments": None}
    comments = Comment.objects.filter(salon_or_service_id=service.service_id, type=1).order_by("-comment_id")
    if comments:
        context_dict["comments"] = comments
        context_dict["comment_count"] = len(comments)
        # Calculate the average rate of the current service
        service.service_rate = round(sum([c.star for c in comments]) / len(comments))
        service.save()
        context_dict["service"] = service
        # context_dict["service_rate"] = service.service_rate
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
            # return redirect(reverse('salonrate:service'))
            return redirect(reverse('salonrate:service', kwargs={'service_name_slug': service_name_slug}))
        else:
            print(form.errors)
    context_dict['form'] = form
    return render(request, 'salonrate/service.html', context_dict)


def search_result(request):
    return render(request, 'salonrate/search_result.html')


def ajax_search(request):
    scope = request.POST.get("scope")
    keyword = request.POST.get('keyword')

    # init search detail object
    search_detail = None

    # search in salon scope
    if scope == "salon":
        # prefilter to get which tag filters selected
        pre_filters = {
            'good_env': request.POST.get('sort_tag[good_env]'),
            'good_service': request.POST.get('sort_tag[good_service]'),
            'cost_effective': request.POST.get('sort_tag[cost_effective]'),
            'good_skill': request.POST.get('sort_tag[good_skill]'),
            'good_attitude': request.POST.get('sort_tag[good_attitude]'),
            'not_busy': request.POST.get('sort_tag[not_busy]')
        }
        # create customized where limit conditions(where xxx=xxx)
        filters = {}
        for k, v in pre_filters.items():
            # if tag is selected, add to where limit conditions
            if v is not None:
                if k is "not_busy":
                    filters["salon_busy"] = 1 if v == 1 else 0
                else:
                    filters[k] = v
        search_detail = Salon.objects.filter(salon_name__contains=keyword)
        # query with dynamic where limit conditions
        search_detail = search_detail.filter(**filters)

    else:
        # prefilter to get which tag filters selected
        pre_filters = {
            'wash': request.POST.get('sort_tag[wash]'),
            'cut': request.POST.get('sort_tag[cut]'),
            'dye': request.POST.get('sort_tag[dye]'),
            'perm': request.POST.get('sort_tag[perm]'),
            'care': request.POST.get('sort_tag[care]'),
        }
        # map type name to integer used in database
        service_tag_map = {'wash': 0, 'cut': 1, 'dye': 2, 'perm': 3, 'care': 4}
        sort_type = []
        for k, v in pre_filters.items():
            if v is not None:
                sort_type.append(service_tag_map.get(k))

        # create default query with name conditions
        search_detail = Service.objects.filter(service_name__contains=keyword)
        # use Q query to create dynamic where limit conditions
        q_query = Q()
        for i in range(len(sort_type)):
            # if tag is selected, add it into where limit conditions by *OR*
            # i.e. tag_condition1 OR tag_condition2 OR ...
            q_query |= Q(service_type=sort_type[i])

        # update default querySet with dynamic Q where limit conditions
        # i.e. select * from service where service_name like "%xxx%" AND (tag1 OR tag2 OR tag3 ...)
        search_detail = search_detail.filter(q_query)

    # map object to json format
    res = serializers.serialize('json', search_detail)
    return HttpResponse(res)

# def jsonEncoder(data):
#     json_data = []
#     for p in data:
#         print(p.__dict__)
#         p.__dict__.pop("_state") # Remove '_state'
#         json_data.append(p.__dict__) 
#     return json_data
