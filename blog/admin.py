from django.contrib import admin

from blog.models import BlogPost, Category

admin.site.register(BlogPost)
admin.site.register(Category)

