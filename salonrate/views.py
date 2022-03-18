import json
from django.shortcuts import get_object_or_404, render
from salonrate.models import UserProfile, Salon, Service, Comment, Follows
from django.core import serializers
from salonrate.forms import CommentForm, UserForm, UserProfileForm
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


@login_required
def user_profile(request):
    user = request.user
    profile = UserProfile.objects.filter(user=user)[0]
    follows = Follows.objects.filter(username=user)
    print("follows: ", len(follows))
    context_dic = {'username': request.user.username, 'profile':profile, 'follows': follows}
    return render(request, 'salonrate/userprofile.html', context_dic)


def homepage(request):
    sql = "SELECT * FROM salonrate_salon WHERE rate >=3 ORDER BY random() LIMIT 3"
    salons = Salon.objects.raw(sql)
    context_dict = {"salons":salons}
    return render(request, 'salonrate/homepage.html', context_dict)


def salon_detail(request, salon_name_slug="rich-hair-beauty-salon"):
    salon = get_object_or_404(Salon, slug=salon_name_slug)
    context_dict = {"salon": salon, "services": None, "comments": None, "follow":False}
    
    comments = Comment.objects.filter(salon_or_service_id=salon.salon_id, type=0).order_by("-comment_id")
    if comments:
        context_dict["comments"] = comments
        context_dict["comment_count"] = len(comments)
        salon.rate = round(sum([c.star for c in comments]) / len(comments))
        salon.save()
        context_dict["salon"] = salon
        context_dict["rate"] = salon.rate
    else:
        print("No Comments")

    services = Service.objects.filter(salon_id = salon.salon_id).order_by("-service_id")
    if services:
        context_dict["services"] = services
    else:
        print("No services available yet")

    if request.user.is_authenticated:
        follows = Follows.objects.filter(username=request.user)
        for follow in follows:
            if follow.salon_id == salon:
                context_dict["follow"]=True
    # print(context_dict["follow"])

    commentform = CommentForm()
    # print(commentform)

    if request.method == 'POST':
        if 'comment' in request.POST:
            commentform = CommentForm(request.POST)
            # print(commentform)
            if commentform.is_valid():
                comment = commentform.save(commit=False)
                comment.username = request.user
                comment.salon_or_service_id = salon.salon_id
                comment.type = 0
                comment.save()
                if comment.tag_environ == True:
                    salon.good_env = True
                if comment.tag_service == True:
                    salon.good_service = True
                if comment.tag_cost == True:
                    salon.cost_effective = True
                if comment.tag_skill == True:
                    salon.good_skill = True 
                if comment.tag_attitude == True:
                    salon.good_attitude = True 
                salon.save()
            return redirect(reverse("salonrate:salon", kwargs={"salon_name_slug": salon_name_slug}))

        else:
            print('followForm detected')
            if context_dict["follow"]==True:
                follows = Follows.objects.filter(username=request.user, salon_id = salon)
                for f in follows:
                    f.delete()
                print('follow deleted')
            else:
                follow = Follows(username=request.user, salon_id=salon)
                follow.save()
                print('follow saved')
            return redirect(reverse("salonrate:salon", kwargs={"salon_name_slug": salon_name_slug}))
    context_dict['form'] = commentform
    return render(request, 'salonrate/salon.html', context_dict)


def service_detail(request, service_name_slug="eyebrows-eyelashes-191"):
    service = get_object_or_404(Service, slug=service_name_slug)
    context_dict = {"service": service, "comments": None}
    comments = Comment.objects.filter(salon_or_service_id=service.service_id, type=1).order_by("-comment_id")
    if comments:
        context_dict["comments"] = comments
        context_dict["comment_count"] = len(comments)
        # Calculate the average rate of the current service
        service.rate = round(sum([c.star for c in comments]) / len(comments))
        service.save()
        context_dict["service"] = service
        # context_dict["service_rate"] = service.service_rate
    else:
        print("No Comments")

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)

        print(form)
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
    para_count = len(request.POST)
    # print(para_count)
    if para_count <= 4:
        print('Non ajax')
        scope = request.POST.get("scope")
        keyword = request.POST.get('keyword')

        # print(f"{scope}::{keyword}")
        # init search detail object
        search_detail = None
        if scope is None:
            scope = ""
        if keyword is None:
            keyword = ""

        # keyword = "hair"

        # search in salon scope
        if scope == "salon":
            search_detail = Salon.objects.filter(salon_name__contains=keyword)

        else:
            # create default query with name conditions
            search_detail = Service.objects.filter(service_name__contains=keyword)

        search_detail = search_detail.order_by("-rate")
        paginator = Paginator(search_detail, 6)
        if request.method == 'POST' and not request.is_ajax():
            page = paginator.page(1)

            return render(request, 'salonrate/search_result.html', {'scope': scope, 'keyword': keyword, 'detail': page})

        if request.is_ajax():
            current_page = int(request.POST.get('current_page'))
            page = paginator.page(current_page)
            # print(page)
            # page_li = list(page.object_list.values())
            # result = {
            #     'has_previous': page.has_previous(),
            #     'has_next': page.has_next(),
            #     'num_pages': page.paginator.num_pages,
            #     'user_li': page_li
            # }
            # print(result)
            return render(request, 'salonrate/ajax_search.html', {'scope': scope, 'keyword': keyword, 'detail': page})
    else:
        return ajax_search(request)

    # context_dict = {'scope': scope, 'detail': search_detail}
    # print(context_dict)
    # # return HttpResponse(render_to_string('salonrate/search_result.html',context_dict))
    # return render(request, 'salonrate/search_result.html', context_dict)


def ajax_search(request):
    # para_count = len(request.POST)
    # print(para_count)
    print("Ajax")
    scope = request.POST.get("scope")
    keyword = request.POST.get('keyword')
    current_page = int(request.POST.get('current_page'))


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
                if k == "not_busy":
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

    search_detail = search_detail.order_by("-rate")
    paginator = Paginator(search_detail, 6)
    page = paginator.page(current_page)
    print(page)
    return render(request, 'salonrate/ajax_search.html', {'scope': scope, 'keyword': keyword, 'detail': page})
    # map object to json format
    # res = serializers.serialize('json', search_detail)
    # return HttpResponse(res)

# def jsonEncoder(data):
#     json_data = []
#     for p in data:
#         print(p.__dict__)
#         p.__dict__.pop("_state") # Remove '_state'
#         json_data.append(p.__dict__) 
#     return json_data
