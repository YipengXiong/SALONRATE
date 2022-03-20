from django.test import SimpleTestCase
from django.urls import reverse, resolve
from salonrate.views import homepage, salon_detail, service_detail, search_result, ajax_search, user_profile, register, user_login, user_logout
class TestUrls(SimpleTestCase):

    def test_homepage_url_is_resolved(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)

    def test_salon_url_is_resolved(self):
        url = reverse('salonrate:salon', kwargs={'salon_name_slug':'inhype-beauty'})
        self.assertEquals(resolve(url).func, salon_detail)

    def test_service_url_is_resolved(self):
        url = reverse('salonrate:service', args=['hair-colouring-3'])
        self.assertEquals(resolve(url).func, service_detail)

    def test_search_result_url_is_resolved(self):
        url = reverse('salonrate:search_result')
        self.assertEquals(resolve(url).func, search_result)

    def test_ajax_search_url_is_resolved(self):
        url = reverse('salonrate:ajax_search')
        self.assertEquals(resolve(url).func, ajax_search)

    def test_register_url_is_resolved(self):
        url = reverse('salonrate:register')
        self.assertEquals(resolve(url).func, register)

    def test_login_url_is_resolved(self):
        url = reverse('salonrate:login')
        self.assertEquals(resolve(url).func, user_login)
    
    def test_logout_url_is_resolved(self):
        url = reverse('salonrate:logout')
        self.assertEquals(resolve(url).func, user_logout)

    def test_profile_url_is_resolved(self):
        url = reverse('salonrate:profile')
        self.assertEquals(resolve(url).func, user_profile)