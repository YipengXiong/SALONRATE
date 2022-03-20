from django.test import TestCase, Client
from django.urls import reverse
from salonrate.models import Salon, Service, Comment, Follows, UserProfile
from django.contrib.auth.models import User
import json

from salonrate.views import register

class TestViews(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        profile = UserProfile.objects.create(user=self.user)
        profile.save()
        self.salon = Salon.objects.create(salon_name="Dunaskin Mill Salon", rate=4,
                                     salon_address="5 Dunaskin Court, Glasgow, G11 6EQ", salon_avg_price=32.3,
                                     phone="0756555443")
        self.salon.save()  # salon_name_slug="dunaskin-mill-salon"
        service = Service.objects.create(service_name="Wash Hair", salon_id=self.salon, service_type=0, service_price=6.6)
        service.save()  # service_name_slug="wash-hair-1"
        service_1 = Service.objects.create(service_name="Cut Hair", salon_id=self.salon, service_type=1, service_price=16.6)
        service_1.save()  # service_name_slug="cut-hair-2"
        service_2 = Service.objects.create(service_name="Dye Hair", salon_id=self.salon, service_type=2, service_price=48.8)
        service_2.save()  # service_name_slug="dye-hair-3"
        service_3 = Service.objects.create(service_name="Perm Hair", salon_id=self.salon, service_type=3, service_price=58.8)
        service_3.save()  # service_name_slug="perm-hair-4"
        service_4 = Service.objects.create(service_name="Hair Care", salon_id=self.salon, service_type=4, service_price=28.8)
        service_4.save()  # service_name_slug="hair-care-5"
        service_5 = Service.objects.create(service_name="Beauty Care", salon_id=self.salon, service_type=4,
                                           service_price=58.8)
        service_5.save()  # service_name_slug="beauty-care-6"
        service_6 = Service.objects.create(service_name="Wax", salon_id=self.salon, service_type=4, service_price=18.8)
        service_6.save()  # service_name_slug="wax-7"
        service_7 = Service.objects.create(service_name="Eyebrow Care", salon_id=self.salon, service_type=4,
                                           service_price=28.8)
        service_7.save()  # service_name_slug="eyebrow-care-8"
        comment_salon = Comment.objects.create(username=self.user, salon_or_service_id=self.salon.salon_id, type=0,
                                               comment="Went here last Sunday with friends. Perfect experience.",
                                               star=3,
                                               tag_environ=True, tag_service=True, tag_skill=True)
        comment_salon.save()
        comment_salon1 = Comment.objects.create(username=self.user, salon_or_service_id=self.salon.salon_id, type=0,
                                                comment="Test comment 1", star=1,
                                                tag_environ=True)
        comment_salon1.save()
        comment_salon2 = Comment.objects.create(username=self.user, salon_or_service_id=self.salon.salon_id, type=0,
                                                comment="Test comment 2", star=2,
                                                tag_environ=True, tag_service=True)
        comment_salon2.save()
        comment_salon3 = Comment.objects.create(username=self.user, salon_or_service_id=self.salon.salon_id, type=0,
                                                comment="Test comment 3", star=3,
                                                tag_environ=True, tag_service=True, tag_attitude=True)
        comment_salon3.save()
        comment_salon4 = Comment.objects.create(username=self.user, salon_or_service_id=self.salon.salon_id, type=0,
                                                comment="Test comment 4", star=4,
                                                tag_environ=True, tag_service=True, tag_skill=True, tag_attitude=True)
        comment_salon4.save()
        comment_service = Comment.objects.create(username=self.user, salon_or_service_id=service.service_id, type=1,
                                                 comment="My hair looks good!", star=4)
        comment_service.save()
        comment_service1 = Comment.objects.create(username=self.user, salon_or_service_id=service.service_id, type=1,
                                                  comment="Test comment service 1.", star=1)
        comment_service1.save()
        comment_service2 = Comment.objects.create(username=self.user, salon_or_service_id=service.service_id, type=1,
                                                  comment="Test comment service 2.", star=2)
        comment_service2.save()
        comment_service3 = Comment.objects.create(username=self.user, salon_or_service_id=service.service_id, type=1,
                                                  comment="Test comment service 3.", star=3)
        comment_service3.save()
        comment_service4 = Comment.objects.create(username=self.user, salon_or_service_id=service.service_id, type=1,
                                                  comment="Test comment service 4.", star=4)
        comment_service4.save()
        comment_service5 = Comment.objects.create(username=self.user, salon_or_service_id=service.service_id, type=1,
                                                  comment="Test comment service 5.", star=5)
        comment_service5.save()
        follow = Follows.objects.create(username=self.user, salon_id=self.salon)
        follow.save()

        user1 = User.objects.create(username='test1')
        user1.set_password('test1')
        user1.save()
        profile1 = UserProfile.objects.create(user=user1)
        profile1.save()
        self.salon1 = Salon.objects.create(salon_name="West Village Salon", rate=4,
                                      salon_address="1 Beith St, Glasgow, G11 6PS", salon_avg_price=15.8,
                                      phone="07126658995", salon_busy=True)
        self.salon1.save()  # salon_name_slug="west-village-salon"
        service1 = Service.objects.create(service_name="Wash Hair", salon_id=self.salon1, service_type=0, service_price=5)
        service1.save()  # service_name_slug="wash-hair-9"
        service1_1 = Service.objects.create(service_name="Beauty Care", salon_id=self.salon1, service_type=4,
                                            service_price=50)
        service1_1.save()  # service_name_slug="beauty-care-10"
        service1_2 = Service.objects.create(service_name="Wax", salon_id=self.salon1, service_type=4, service_price=10)
        service1_2.save()  # service_name_slug="wax-11"
        service1_3 = Service.objects.create(service_name="Eyebrow Care", salon_id=self.salon1, service_type=4,
                                            service_price=20)
        service1_3.save()  # service_name_slug="eyebrow-care-12"
        follow1 = Follows.objects.create(username=self.user, salon_id=self.salon1)
        follow1.save()  # Attention: user follows 2 salons while user1 follow no salon

        salon2 = Salon.objects.create(salon_name="Aparto Salon", rate=5,
                                      salon_address="145 Kelvinhaugh Street, Glasgow", salon_avg_price=15.8,
                                      phone="06453535353", salon_busy=True)
        self.client = Client()
        self.register_url = reverse('salonrate:register')
        self.login_url = reverse('salonrate:login')
        self.homepage_url = reverse('salonrate:homepage')
        self.salon_url = reverse('salonrate:salon', kwargs = {'salon_name_slug':'dunaskin-mill-salon'})
        self.service_url = reverse('salonrate:service', kwargs = {'service_name_slug':'eyebrow-care-8'})
        self.search_result_url = reverse('salonrate:search_result')
        self.profile_url = reverse('salonrate:profile')
        return super().setUp()

    def test_register_get(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'salonrate/register.html')

    def test_register_post(self):
        response = self.client.post(self.register_url, data={
            'username':'lovetest',
            'email':'lovetest@test.com',
            'password':'lovetest',
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'salonrate/register.html')
        self.assertEquals(response.context['registered'], True)

    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'salonrate/login.html')
    
    def test_login_post_invalid_user(self):
        response = self.client.post(self.login_url, data={'username':'', 'password':''})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Invalid login details supplied.")

    def test_salon_detail_get(self):
        response = self.client.get(self.salon_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'salonrate/salon.html')
        self.assertEqual(response.context['salon'].salon_id, 1)
        self.assertEqual(response.context['salon'].salon_name, 'Dunaskin Mill Salon')
        self.assertEqual(response.context['salon'].salon_address, '5 Dunaskin Court, Glasgow, G11 6EQ')
        self.assertEqual(response.context['salon'].phone, '0756555443')
        self.assertEqual(response.context['salon'].salon_avg_price, 32.3)
        self.assertEqual(len(response.context['services']), 8)
        self.assertEqual(len(response.context['comments']), 5)
    
    def test_service_detail_get(self):
        response = self.client.get(self.service_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'salonrate/service.html')
    
    def test_profile_get(self):
        self.client.login(username='test', password='test')
        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'salonrate/userprofile.html')
    
    def test_empty_userprofile_class(self):
        c = Client()
        c.login(username='test1', password='test1')
        response = c.get(reverse('salonrate:profile'))
        self.assertContains(response, 'No Comments Yet~')
        self.assertContains(response, 'No Follows Yet~')
    
    def test_homepage_get(self):
        response = self.client.get(self.homepage_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'salonrate/homepage.html')

    def test_non_ajax_search_salon(self):
        c = Client()
        c.login(username='test', password='test')
        response = self.client.post(reverse('salonrate:search_result'), {'scope': 'salon', 'keyword': 'dunaskin'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['detail'][0].salon_id, 1)
        self.assertEqual(response.context['detail'][0].salon_name, 'Dunaskin Mill Salon')
        self.assertEqual(response.context['detail'][0].salon_address, '5 Dunaskin Court, Glasgow, G11 6EQ')
        self.assertEqual(response.context['detail'][0].phone, '0756555443')
        self.assertEqual(response.context['detail'][0].salon_avg_price, 32.3)

    def test_non_ajax_search_service(self):
        c = Client()
        c.login(username='test', password='test')
        response = self.client.post(reverse('salonrate:search_result'), {'scope': 'service', 'keyword': 'wash hair'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['detail'][0].service_id, 1)
        self.assertEqual(response.context['detail'][0].service_name, 'Wash Hair')
        self.assertEqual(response.context['detail'][0].salon_id.salon_id, 1)
        self.assertEqual(response.context['detail'][0].service_type, 0)
        self.assertEqual(response.context['detail'][0].service_price, 6.6)

    def test_ajax_search_salon(self):
        c = Client()
        c.login(username='test', password='test')
        response = self.client.post(reverse('salonrate:ajax_search'),
                                    {'scope': 'salon', 'keyword': 'dunaskin', 'current_page': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['detail'][0].salon_id, 1)
        self.assertEqual(response.context['detail'][0].salon_name, 'Dunaskin Mill Salon')
        self.assertEqual(response.context['detail'][0].salon_address, '5 Dunaskin Court, Glasgow, G11 6EQ')
        self.assertEqual(response.context['detail'][0].phone, '0756555443')
        self.assertEqual(response.context['detail'][0].salon_avg_price, 32.3)

    def test_ajax_search_service(self):
        c = Client()
        c.login(username='test', password='test')
        response = self.client.post(reverse('salonrate:ajax_search'),
                                    {'scope': 'service', 'keyword': 'wash hair', 'current_page': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['detail'][0].service_id, 1)
        self.assertEqual(response.context['detail'][0].service_name, 'Wash Hair')
        self.assertEqual(response.context['detail'][0].salon_id.salon_id, 1)
        self.assertEqual(response.context['detail'][0].service_type, 0)
        self.assertEqual(response.context['detail'][0].service_price, 6.6)