from django.test import SimpleTestCase
from django.contrib.auth.models import User
from salonrate.models import Salon, Service, Comment, Follows, UserProfile


class TestModels(SimpleTestCase):
    allow_database_queries=True

        # self.user = User.objects.create(username='lovetest', password='lovetest', email='lovetest@t.com')
        # self.profile = UserProfile.objects.create(user=self.user)
        # self.profile.save()
        
        
        # comment_salon = Comment.objects.create(username=self.user, salon_or_service_id=self.salon.salon_id, type=0,
        #                                   comment="Went here last Sunday with friends. Perfect experience.", star=3,
        #                                   tag_environ=True, tag_service=True, tag_skill=True)
        # comment_salon.save()

        # comment_service = Comment.objects.create(username=self.user, salon_or_service_id=self.service.service_id, type=1,
        #                                   comment="My hair looks good!", star=4)
        # comment_service.save()
        # follow = Follows.objects.create(username=self.user,salon_id=self.salon)
        # follow.save()

    def test_salon_is_assigned_slug(self):
        self.salon = Salon.objects.create(salon_name="Dunaskin Mill Salon", rate=4,
                                     salon_address="5 Dunaskin Court, Glasgow, G11 6EQ", salon_avg_price=32.3,
                                     phone="0756555443")
        self.salon.save()    # salon_name_slug="dunaskin-mill-salon"
        self.assertEquals(self.salon.slug, "dunaskin-mill-salon")
    
    def test_service_is_assigned_slug(self):
        self.service = Service.objects.create(service_name="Dye Hair", salon_id=self.salon, service_type=0, service_price=6.6)
        self.service.save()  # service_name_slug="dye-hair-1"
        self.assertEquals(self.service.slug, "dye-hair-1")