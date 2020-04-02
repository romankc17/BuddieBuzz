from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image as pilImage

class Post(models.Model):
    caption= models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.id})

def get_image_filename(instance, filename):
    id = instance.post.id
    return "post_images/%s" % (id)


class Image(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)

        img = pilImage.open(self.image.path)

        if img.height > 640 or img.width > 320:
            output_size = (640, 320)
            img.thumbnail(output_size)
            img.save(self.image.path)
