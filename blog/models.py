from pyexpat import model
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings

from ckeditor.fields import RichTextField


def get_header_image_filepath(self, filename):
    return f'header_images/{self.pk}/{filename}'



class Category(models.Model):
    name                    = models.CharField(max_length=35, unique=True)

    def __str__(self):
        return self.name
    

class BlogPost(models.Model):
    title                   = models.CharField(max_length=50, null=False, blank=False)
    body                    = RichTextField(blank=True, null=True)
    category                = models.ForeignKey(Category, on_delete=models.CASCADE)
    header_image            = models.ImageField(max_length=255, upload_to=get_header_image_filepath, null=True, blank=True)
    video                   = models.FileField(null=True, blank=True, upload_to="videos/%y")
    date_published          = models.DateTimeField(auto_now_add=True, verbose_name='date published')
    date_updated            = models.DateTimeField(auto_now=True, verbose_name='date updated')
    author                  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug                    = models.SlugField(blank=True, unique=True)

    
    def __str__(self):
        return self.title


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)







