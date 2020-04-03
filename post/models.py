import random
import string

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image as pilImage
from django.utils.text import slugify




def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class Post(models.Model):
    caption= models.TextField(max_length=500)
    slug = models.SlugField(max_length=20, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        while True:
            slug = randomString()
            existed_slug = [post.slug for post in Post.objects.all()]
            if (slug in existed_slug):
                pass
            else:
                self.slug = slug
                break
        super(Post, self).save(*args, **kwargs,)


    def likedby(self, user):
        self.likes.add(user)

    def unlikedby(self, user):
        self.likes.remove(user)

    def is_likedby(self, user):
        return (user in self.likes.all())


    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.id})



def get_image_filename(instance, filename):
    id = instance.post.id
    return "post_images/%s" % (id)


class Image(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              null = True,
                              blank=True,
                              verbose_name='Image')

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)

        img = pilImage.open(self.image.path)

        if img.height > 200 or img.width > 100:
            output_size = (200, 100)
            img.thumbnail(output_size)
            img.save(self.image.path)

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  related_name='comments', )
    commenter = models.ForeignKey(User, on_delete=models.CASCADE,  )
    body = models.TextField(max_length=300)
    likes = models.ManyToManyField(User, blank=True, related_name='like')
    post_comment_created = models.DateTimeField(auto_now_add=True)
    post_comment_updated = models.DateTimeField(auto_now=True, null=True)