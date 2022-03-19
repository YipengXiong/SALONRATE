from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
import salonrate
from salonrate import models
from salonrate.models import UserProfile, Comment, Salon, Service, Follows


def create_user_object():
    user = User.objects.create(username='testuser')
    user.set_password('test123456')
    user.save()
    userprofile = UserProfile.objects.create(user)


class salonratemodeltest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        profile = UserProfile.objects.create(user=user)
        profile.save()
        salon = Salon.objects.create(salon_name="Dunaskin Mill Salon", rate=4,
                                     salon_address="5 Dunaskin Court, Glasgow, G11 6EQ", salon_avg_price=13.6,
                                     phone="0756555443")
        salon.save()    # salon_name_slug="dunaskin-mill-salon"
        service = Service.objects.create(service_name="Cut Hair", salon_id=salon, service_type=1, service_price=15.6)
        service.save()  # service_name_slug="cut-hair-1"
        comment_salon = Comment.objects.create(username=user, salon_or_service_id=salon.salon_id, type=0,
                                          comment="Went here last Sunday with friends. Perfect experience.", star=3,
                                          tag_environ=True, tag_service=True, tag_skill=True, tag_attitude=True)
        comment_salon.save()
        comment_service = Comment.objects.create(username=user, salon_or_service_id=service.service_id, type=1,
                                          comment="My hair looks good!", star=4)
        comment_service.save()
        follow = Follows.objects.create(username=user,salon_id=salon)
        follow.save()

        user1 = User.objects.create(username='test1')
        user1.set_password('test1')
        user1.save()
        profile1 = UserProfile.objects.create(user=user1)
        profile1.save()
        salon1 = Salon.objects.create(salon_name="West Village Salon", rate=4,
                                     salon_address="1 Beith St, Glasgow, G11 6PS", salon_avg_price=15.8,
                                     phone="07126658995")
        salon1.save()   # salon_name_slug="west-village-salon"
        service1 = Service.objects.create(service_name="Wash Hair", salon_id=salon, service_type=0, service_price=15.6)
        service1.save()     # service_name_slug="wash-hair-2"
        comment_salon_1 = Comment.objects.create(username=user1, salon_or_service_id=salon1.salon_id, type=0,
                                          comment="Went here last Sunday with friends. Perfect experience.", star=3,
                                          tag_environ=True, tag_service=True, tag_skill=True, tag_attitude=True)
        comment_salon_1.save()
        comment_service_1 = Comment.objects.create(username=user1, salon_or_service_id=service1.service_id, type=1,
                                          comment="My hair looks good!", star=4)
        comment_service_1.save()
        follow1 = Follows.objects.create(username=user1,salon_id=salon1)
        follow1.save()
        follow1_1 = Follows.objects.create(username=user,salon_id=salon1)
        follow1_1.save()
        return super().setUp()

    def test_userprofile_class(self):
        user = User.objects.create(username='test1')
        user.set_password('test1')
        user.save()

        profile = UserProfile.objects.create(user=user)
        profile.save()

        salon = Salon.objects.create(salon_name="Dunaskin Mill Salon", rate=4,
                                     salon_address="5 Dunaskin Court, Glasgow, G11 6EQ", salon_avg_price=13.6,
                                     phone="0756555443")
        salon.save()

        service = Service.objects.create(service_name="Cut Hair", salon_id=salon, service_type=1, service_price=15.6)
        service.save()

        comment1 = Comment.objects.create(username=user, salon_or_service_id=salon.salon_id, type=0,
                                          comment="Went here last Sunday with friends. Perfect experience.", star=3,
                                          tag_environ=True, tag_service=True, tag_skill=True, tag_attitude=True)
        comment1.save()

        comment2 = Comment.objects.create(username=user, salon_or_service_id=service.service_id, type=1,
                                          comment="My hair looks good!", star=4)
        comment2.save()

        follow = Follows.objects.create(username=user,salon_id=salon)
        follow.save()

        c = Client()
        c.login(username='test1', password='test1')
        response = c.get(reverse('salonrate:profile'))
        print(response.context['username'])
        print(response.context['profile'])
        print(response.context['comments'])
        print(response.context['follows'])
