from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
import salonrate
from salonrate import models
from salonrate.models import UserProfile, Comment, Salon, Service, Follows

class salonratemodeltest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        profile = UserProfile.objects.create(user=user)
        profile.save()
        salon = Salon.objects.create(salon_name="Dunaskin Mill Salon", rate=4,
                                     salon_address="5 Dunaskin Court, Glasgow, G11 6EQ", salon_avg_price=32.3,
                                     phone="0756555443")
        salon.save()    # salon_name_slug="dunaskin-mill-salon"
        service = Service.objects.create(service_name="Wash Hair", salon_id=salon, service_type=0, service_price=6.6)
        service.save()  # service_name_slug="wash-hair-1"
        service_1 = Service.objects.create(service_name="Cut Hair", salon_id=salon, service_type=1, service_price=16.6)
        service_1.save()    # service_name_slug="cut-hair-2"
        service_2 = Service.objects.create(service_name="Dye Hair", salon_id=salon, service_type=2, service_price=48.8)
        service_2.save()    # service_name_slug="dye-hair-3"
        service_3 = Service.objects.create(service_name="Perm Hair", salon_id=salon, service_type=3, service_price=58.8)
        service_3.save()    # service_name_slug="perm-hair-4"
        service_4 = Service.objects.create(service_name="Hair Care", salon_id=salon, service_type=4, service_price=28.8)
        service_4.save()    # service_name_slug="hair-care-5"
        service_5 = Service.objects.create(service_name="Beauty Care", salon_id=salon, service_type=4, service_price=58.8)
        service_5.save()    # service_name_slug="beauty-care-6"
        service_6 = Service.objects.create(service_name="Wax", salon_id=salon, service_type=4, service_price=18.8)
        service_6.save()    # service_name_slug="wax-7"
        service_7 = Service.objects.create(service_name="Eyebrow Care", salon_id=salon, service_type=4, service_price=28.8)
        service_7.save()    # service_name_slug="eyebrow-care-8"
        comment_salon = Comment.objects.create(username=user, salon_or_service_id=salon.salon_id, type=0,
                                          comment="Went here last Sunday with friends. Perfect experience.", star=3,
                                          tag_environ=True, tag_service=True, tag_skill=True)
        comment_salon.save()
        comment_salon1 = Comment.objects.create(username=user, salon_or_service_id=salon.salon_id, type=0,
                                          comment="Test comment 1", star=1,
                                          tag_environ=True)
        comment_salon1.save()
        comment_salon2 = Comment.objects.create(username=user, salon_or_service_id=salon.salon_id, type=0,
                                          comment="Test comment 2", star=2,
                                          tag_environ=True, tag_service=True)
        comment_salon2.save()
        comment_salon3 = Comment.objects.create(username=user, salon_or_service_id=salon.salon_id, type=0,
                                          comment="Test comment 3", star=3,
                                          tag_environ=True, tag_service=True, tag_attitude=True)
        comment_salon3.save()
        comment_salon4 = Comment.objects.create(username=user, salon_or_service_id=salon.salon_id, type=0,
                                          comment="Test comment 4", star=4,
                                          tag_environ=True, tag_service=True, tag_skill=True, tag_attitude=True)
        comment_salon4.save()
        comment_service = Comment.objects.create(username=user, salon_or_service_id=service.service_id, type=1,
                                          comment="My hair looks good!", star=4)
        comment_service.save()
        comment_service1 = Comment.objects.create(username=user, salon_or_service_id=service.service_id, type=1,
                                          comment="Test comment service 1.", star=1)
        comment_service1.save()
        comment_service2 = Comment.objects.create(username=user, salon_or_service_id=service.service_id, type=1,
                                          comment="Test comment service 2.", star=2)
        comment_service2.save()
        comment_service3 = Comment.objects.create(username=user, salon_or_service_id=service.service_id, type=1,
                                          comment="Test comment service 3.", star=3)
        comment_service3.save()
        comment_service4 = Comment.objects.create(username=user, salon_or_service_id=service.service_id, type=1,
                                          comment="Test comment service 4.", star=4)
        comment_service4.save()
        comment_service5 = Comment.objects.create(username=user, salon_or_service_id=service.service_id, type=1,
                                          comment="Test comment service 5.", star=5)
        comment_service5.save()
        follow = Follows.objects.create(username=user,salon_id=salon)
        follow.save()

        user1 = User.objects.create(username='test1')
        user1.set_password('test1')
        user1.save()
        profile1 = UserProfile.objects.create(user=user1)
        profile1.save()
        salon1 = Salon.objects.create(salon_name="West Village Salon", rate=4,
                                     salon_address="1 Beith St, Glasgow, G11 6PS", salon_avg_price=15.8,
                                     phone="07126658995", salon_busy=True)
        salon1.save()   # salon_name_slug="west-village-salon"
        service1 = Service.objects.create(service_name="Wash Hair", salon_id=salon1, service_type=0, service_price=5)
        service1.save()     # service_name_slug="wash-hair-9"
        service1_1 = Service.objects.create(service_name="Beauty Care", salon_id=salon1, service_type=4, service_price=50)
        service1_1.save()    # service_name_slug="beauty-care-10"
        service1_2 = Service.objects.create(service_name="Wax", salon_id=salon1, service_type=4, service_price=10)
        service1_2.save()    # service_name_slug="wax-11"
        service1_3 = Service.objects.create(service_name="Eyebrow Care", salon_id=salon1, service_type=4, service_price=20)
        service1_3.save()    # service_name_slug="eyebrow-care-12"
        follow1 = Follows.objects.create(username=user,salon_id=salon1)
        follow1.save()  # Attention: user follows 2 salons while user1 follow no salon
        return super().setUp()

    def test_userprofile_class(self):
        c = Client()
        c.login(username='test1', password='test1')
        response = c.get(reverse('salonrate:profile'))
        print(response.context['username'])
        print(response.context['profile'])
        print(response.context['comments'])
        print(response.context['follows'])

    def test_salon_detail_unauthorized(self):
        response = self.client.get(reverse('salonrate:salon', kwargs={'salon_name_slug':'dunaskin-mill-salon'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['salon'].salon_id, 1)
        self.assertEqual(response.context['salon'].salon_name, 'Dunaksin Mill Salon')
        self.assertEqual(response.context['salon'].salon_address, '5 Dunaskin Court, Glasgow, G11 6EQ')
        self.assertEqual(response.context['salon'].phone, '0756555443')
        self.assertEqual(response.context['salon'].salon_avg_price, 32.3)
        self.assertEqual(len(response.context['services']), 8)
        self.assertEqual(len(response.context['comments']), 5)

    def test_salon_detail_authorized(self):
        c = Client()
        c.login(username='test', password='test')
        response = self.client.get(reverse('salonrate:salon', kwargs={'salon_name_slug':'dunaskin-mill-salon'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['salon'].salon_id, 1)
        self.assertEqual(response.context['salon'].salon_name, 'Dunaksin Mill Salon')
        self.assertEqual(response.context['salon'].salon_address, '5 Dunaskin Court, Glasgow, G11 6EQ')
        self.assertEqual(response.context['salon'].phone, '0756555443')
        self.assertEqual(response.context['salon'].salon_avg_price, 32.3)
        self.assertEqual(len(response.context['services']), 8)
        self.assertEqual(len(response.context['comments']), 5)
        self.assertEqual(response.context['follow'], True)