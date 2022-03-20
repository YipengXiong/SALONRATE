import email
import os
import profile
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech_cw_group_17.settings')
import django
django.setup()

from salonrate.models import Service, Salon, Follows, UserProfile, Comment
import json
import random
from django.contrib.auth.models import User


#generate data from json files
def populate_saloninfo():
    open_time_list=["10:00am-5:00pm","09:00am-4:00pm","10:00am-6:00pm"]
    with open("salon_info.json","r") as f:
        salon_info_list = json.load(f)
        #salon_url = salon_info.keys()
        for salon_info in salon_info_list:
            info = list(salon_info.values())[0]
            #print("info:",info)
            salon_name = info[0]["name"]
            salon_rate = info[1]["rate"]
            salon_address = info[2]["address"]
            salon_price = float(random.randint(150, 500)) / 10
            #salon_busy_base = random.randint(0,1)
            salon_busy = False
            if 1 == random.randint(0,1):
                salon_busy=True
            salon_phone = "0000000" + str(random.randint(0,999))
            salon_time = open_time_list[random.randint(0,2)]
            
            #print(salon_name, salon_rate, salon_address, salon_price, salon_busy, salon_phone, salon_time)
            s = Salon(salon_name=salon_name, rate=salon_rate, salon_address=salon_address, salon_avg_price=salon_price, salon_busy=salon_busy, phone=salon_phone, open_time=salon_time)
            s.save()
        f.close()

def populate_service():
    with open("details.json","r") as f:
        salon_detail_list = json.load(f)
        salon_id = 1
        for salon_detail in salon_detail_list:
            detail = list(salon_detail.values())[0]
            salon_object = Salon.objects.filter(salon_id=salon_id)[0]
            
            for name in detail[0]:
                service_name = name[0]["name"]
                #print(service_name)
                service_type = random.randint(0,4)
                service_price = float(random.randint(15, 150))
                service_rate = float(random.randint(0,50)) / 10
                s = Service(salon_id=salon_object, service_name=service_name, service_price=service_price, rate=service_rate, service_type=service_type)
                s.save()
            salon_id = salon_id + 1
        f.close()

def randomBool():
    value = random.randint(0,1)
    if value==0:
        return False
    else:
        return True

def populate_users():
    superuser=User.objects.create_superuser(username="group17", email="group17@group.com", password="group17")
    user=User.objects.create(username="name1", email="name1@name.com", password="name1")
    user.set_password(user.password)
    user.save()
    users=User.objects.all()
    for user in users:
        profile=UserProfile(user=user)
        profile.save()


def populate_comment():
    with open("details.json","r") as f:
        salon_detail_list = json.load(f)
        salons=Salon.objects.all()
        services=Service.objects.all()
        salon_num=len(salons)
        service_num=len(services)
        for salon_detail in salon_detail_list:
            detail = list(salon_detail.values())[0]
            comments = detail[2]['comment']
            for comment in comments:
                comment_type = random.randint(0,1)
                comment_content = comment
                #0 is salon, 1 is service
                id = 0
                if comment_type == 0:
                    id = salons[random.randint(0, salon_num - 1)].salon_id
                else:
                    id = services[random.randint(0, service_num - 1)].service_id
                users = User.objects.all()
                user = users[random.randint(0,1)]
                c = Comment(username=user, salon_or_service_id=id, type=comment_type, comment=comment_content, star=random.randint(0,5),
                            tag_environ=randomBool(), tag_service=randomBool(), tag_cost=randomBool(), tag_skill=randomBool(), tag_attitude=randomBool(),)
                c.save()
        f.close()

def populate_follows():
    users = User.objects.all()
    salons = Salon.objects.all()
    for salon in salons:
        user = users[random.randint(0,1)]
        f = Follows(salon_id=salon, username=user)
        f.save()

#some specific change of data
def revise_stars():
    comments=Comment.objects.all()
    for comment in comments:
        comment.star=random.randint(0,5)
        comment.save()


def revise_avatar():
    profiles=UserProfile.objects.all()
    for profile in profiles:
        profile.avatar="profile_image/default.jpg"
        profile.save()

def refresh_salon(salon, comments):
    if comments:
        salon.rate = round(sum([c.star for c in comments]) / len(comments))
        salon.save()
    else:
        salon.rate = 0
        salon.save()
        
    for comment in comments:
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
    return salon

def refresh_service(service, comments):
    if comments:
        service.rate = round(sum([c.star for c in comments]) / len(comments))
        service.save()
    else:
        service.rate = 0
        service.save()
    return service

def comment_service(comments):
    for comment in comments:
        if comment.tag_environ == True:
            comment.tag_environ = False
            comment.save()
        if comment.tag_service == True:
            comment.tag_service = False
            comment.save()
        if comment.tag_cost == True:
            comment.tag_cost = False
            comment.save()
        if comment.tag_skill == True:
            comment.tag_skill = False
            comment.save()
        if comment.tag_attitude == True:
            comment.tag_attitude = False
            comment.save()
    return

def populate_save():
    salons = Salon.objects.all()
    services = Service.objects.all()
    comments = Comment.objects.filter(type=1)
    comment_service(comments)
    for s in salons:
        comments = Comment.objects.filter(salon_or_service_id=s.salon_id, type=0)
        refresh_salon(s, comments)
    for serv in services:
        comments = Comment.objects.filter(salon_or_service_id=serv.service_id, type=1)
        refresh_service(serv, comments)
    # for c in comments:
    #     c.star = random.randint(1,5)
    #     c.save()
    print("Finished")

if __name__ == '__main__':
    print('Starting population script...')
    # populate_follows()
    # revise_avatar()
    populate_saloninfo()
    populate_service()
    populate_users()
    populate_comment()
    populate_follows()
    populate_save()