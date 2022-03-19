from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
import salonrate
from salonrate import models
from salonrate.models import UserProfile


def create_user_object():
    user = User.objects.create(username='testuser')
    user.set_password('test123456')
    user.save()
    userprofile = UserProfile.objects.create(user)



class salonratemodeltest(TestCase):

    def test_userprofile_class(self):
        response = self.client.get(reverse('salonrate:profile'), kwargs={'username':'testuser'})
        print(response)
        self.assertEqual(response.context['follows'], [])
        # self.assertEqual(response.context['comments'], [])
        self.assertContains(response, "No Follows Yet~")
        self.assertContains(response, "No Comments Yet~")

