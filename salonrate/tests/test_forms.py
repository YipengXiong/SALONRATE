from django.test import SimpleTestCase
from salonrate.forms import UserForm, UserProfileForm, CommentForm
# Create your tests here.

class TestForms(SimpleTestCase):
    allow_database_queries=True

    def test_user_form_valid_data(self):
        form = UserForm(data={
            'username': 'test',
            'email':'test@test.com',
            'password':'test'
        })

        self.assertTrue(form.is_valid())

    def test_user_form_no_data(self):
        form = UserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)
    
    def test_userprofile_form_valid_data(self):
        form = UserProfileForm(data={
            'avatar' : 'media/profile_image/default.jpg',
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_valid_data(self):
        form = CommentForm(data={
            'comment': 'test comment',
            'star':3.0,
            'tag_environ':True,
            'tag_service':True,
            'tag_cost':True,
            'tag_skill':True,
            'tag_attitude': True,
        })

        self.assertTrue(form.is_valid())

    def test_comment_form_no_data(self):
        form = CommentForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)