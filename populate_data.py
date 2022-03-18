import os
import profile
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech_cw_group_17.settings')
import django
django.setup()

from salonrate.models import Service, Salon, Follows, UserProfile, Comment
import json
import random
from django.contrib.auth.models import User

def populate_saloninfo():
    open_time_list=["10:00am-5:00pm","09:00am-4:00pm","10:00am-6:00pm"]
    with open("salon_info.json","r") as f:
        salon_info_list = json.load(f)
        #salon_url = salon_info.keys()
        for salon_info in salon_info_list:
            info = list(salon_info.values())[0]
            print("info:",info)
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
            
            print(salon_name, salon_rate, salon_address, salon_price, salon_busy, salon_phone, salon_time)
            s = Salon(salon_name=salon_name, salon_rate=salon_rate, salon_address=salon_address, salon_avg_price=salon_price, salon_busy=salon_busy, phone=salon_phone, open_time=salon_time)
            s.save()
        f.close()

def populate_service():
    with open("details.json","r") as f:
        salon_detail_list = json.load(f)
        salon_id = 2
        for salon_detail in salon_detail_list:
            detail = list(salon_detail.values())[0]
            salon_object = Salon.objects.filter(salon_id=salon_id)[0]
            
            for name in detail[0]:
                service_name = name[0]["name"]
                print(service_name)
                service_type = random.randint(0,4)
                service_price = float(random.randint(15, 150))
                service_rate = float(random.randint(0,50)) / 10
                s = Service(salon_id=salon_object, service_name=service_name, service_price=service_price, service_rate=service_rate, service_type=service_type)
                s.save()
            salon_id = salon_id + 1
        f.close()

def randomBool():
    value = random.randint(0,1)
    if value==0:
        return False
    else:
        return True

def populate_comment():
    with open("details.json","r") as f:
        salon_detail_list = json.load(f)
        
        for salon_detail in salon_detail_list:
            detail = list(salon_detail.values())[0]
            comments = detail[2]['comment']
            for comment in comments:
                comment_type = random.randint(0,1)
                comment_content = comment
                #0 is salon, 1 is service
                id = 0
                if comment_type == 0:
                    id = random.randint(2, 21)
                else:
                    id = random.randint(1, 193)
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

def populate_save():
    # salons = Salon.objects.all()
    services = Service.objects.all()
    comments = Comment.objects.all()
    # for s in salons:
    #     s.save()
    for serv in services:
        serv.save()
    for c in comments:
        c.star = random.randint(1,5)
        c.save()
    print("Finished")

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


if __name__ == '__main__':
    print('Starting population script...')
    # populate_follows()
    revise_avatar()