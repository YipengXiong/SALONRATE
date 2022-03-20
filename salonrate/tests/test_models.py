from django.test import SimpleTestCase
from django.contrib.auth.models import User
from salonrate.models import Salon, Service, Comment, Follows, UserProfile


class TestModels(SimpleTestCase):
    allow_database_queries=True
    @classmethod
    def setUpClass(clf):
        clf.salon = Salon.objects.create(
            salon_name="Dunaskin Mill Salon", 
            rate=4,
            salon_address="5 Dunaskin Court, Glasgow, G11 6EQ", 
            salon_avg_price=32.3,
            phone="0756555443"
        )
        clf.salon.save()    # salon_name_slug="dunaskin-mill-salon"
        clf.service = Service.objects.create(
            service_name="Dye Hair", 
            salon_id=clf.salon, 
            service_type=0, 
            service_price=6.6
        )
        clf.service.save()  # service_name_slug="dye-hair-1"
        clf.user = User.objects.create(
            username='lovetest', 
            password='lovetest', 
            email='lovetest@t.com'
        )
        clf.userprofile = UserProfile.objects.create(
            user=clf.user,
            avatar='profile_image/default.jpg',
        )
        clf.comment_salon = Comment.objects.create(
            username=clf.user, 
            salon_or_service_id=clf.salon.salon_id, 
            type=0,
            comment="Went here last Sunday with friends. Perfect experience.", 
            star=3,
            tag_environ=True, 
            tag_service=True, 
            tag_skill=True
        )
        clf.comment_service = Comment.objects.create(
            username = clf.user,
            salon_or_service_id = clf.service.service_id,
            type = 0,
            comment = "My hair looks good!",
            star = 4,
            tag_skill = True
        )
        clf.follow = Follows.objects.create(
            username = clf.user,
            salon_id = clf.salon
        )

    def test_salon_is_assigned_slug(self):
        self.assertEquals(self.salon.slug, "dunaskin-mill-salon")
    
    def test_service_is_assigned_slug(self):
        self.assertEquals(self.service.slug, "dye-hair-1")

    def test_user_register(self):
        self.assertEquals(self.user.id, 1)

    def test_userprofile(self):
        self.assertEquals(self.userprofile.id, 1)

    def test_comment_on_salon(self):
        self.assertEquals(self.comment_salon.comment_id, 1)

    def test_comment_on_service(self):
        self.assertEquals(self.comment_service.comment_id, 2)

    def test_follows(self):
        self.assertEquals(self.follow.id, 1)