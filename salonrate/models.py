from email.policy import default
from django.db import models
from django.forms import CharField, FloatField, IntegerField
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# Create your models here.


class Salon(models.Model):
    salon_id = models.AutoField(primary_key=True, null=False)
    salon_name = models.CharField(max_length=50, null=False)
    salon_address = models.CharField(max_length=100, null=False)
    salon_rate = models.FloatField(null=False)
    salon_avg_price = models.FloatField(default=0.0)
    salon_busy = models.BooleanField(default=False)
    image = models.ImageField(upload_to="salon_img", blank=True)
    # tag = models.CharField(max_length=16, default='0')
    phone = models.CharField(max_length=16)
    open_time = models.CharField(max_length=32, default='10:00am-5:00pm')
    slug = models.SlugField(blank=True)
    good_env = models.BooleanField(default=False)
    good_service = models.BooleanField(default=False)
    cost_effective = models.BooleanField(default=False)
    good_skill = models.BooleanField(default=False)
    good_attitude = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.salon_name)
        super(Salon, self).save(*args, **kwargs)

    def __str__(self):
        return self.salon_name


class Service(models.Model):
    service_id = models.AutoField(primary_key=True, null=False)
    salon_id = models.ForeignKey(Salon, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=50, null=False)
    service_type = models.IntegerField(default=0)
    service_price = models.FloatField(default=0.0)
    service_rate = models.FloatField(default=0.0)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.service_name)
        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return self.service_name


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, null=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    #salon_id = models.ForeignKey(Salon, on_delete=models.CASCADE)
    #service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    salon_or_service_id = models.IntegerField(default=0, null=False)
    type = models.IntegerField(default=0)
    comment = models.CharField(max_length=500)
    star = models.IntegerField(default=0)
    tag_environ = models.BooleanField(default=False)
    tag_service = models.BooleanField(default=False)
    tag_cost = models.BooleanField(default=False)
    tag_skill = models.BooleanField(default=False)
    tag_attitude = models.BooleanField(default=False)
    comment_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment_id)


class Follows(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    salon_id = models.ForeignKey(Salon, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username), str(self.salon_id)
    class Meta:
        verbose_name_plural = 'Follows'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to='avatar', blank = True)

    def __str__(self):
        return self.user.username