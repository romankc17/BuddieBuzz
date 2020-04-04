from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from django_countries.fields import CountryField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image= models.ImageField(upload_to='profile_image', default='default.jpg')
    followings = models.ManyToManyField('self', blank=True,default=None, symmetrical=False, related_name='+')
    followers = models.ManyToManyField('self', blank = True,default=None, symmetrical=False,related_name='+')
    bio = models.TextField(max_length=100,blank=True )
    phone_number = models.IntegerField(null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    GENDER = [
        ('M', 'Male'),
        ('F','Female'),
        ('O', 'Other')
    ]
    city = models.CharField(blank=True, null = True, max_length=20)
    country = CountryField(blank_label='SELECT COUNTRY', null=True)
    gender = models.CharField(max_length=1, choices=GENDER, verbose_name='Gender', blank=True)

    def is_friend(self, request_profile):
        return (request_profile in self.followers.all() and request_profile in self.followings.all())

    def follow_to(self, person):
        self.followings.add(person)
        person.followers.add(self)

    def unfollow_to(self, person):
        self.followings.remove(person)
        person.followers.remove(self)

    def follows(self, person):
        return (self in person.followers.all())

    def __str__(self):
        return str(self.user.username)


    def get_absolute_url(self):
        return reverse('profile', kwargs={'the_slug':self.user})

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user = kwargs['instance'])

post_save.connect(create_profile, sender = User)