from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from blog.views import (
    create_blog_view,
    detail_post_view,
    show_category_page_view,
    must_authenticate_view,
)


urlpatterns = [
    path('must-authenticate/', must_authenticate_view, name='must-authenticate'),
    
    path('create_post/', create_blog_view, name='create-post'),
    path('<slug>/', detail_post_view, name='detail-post'),

    path('category/<str:category_name>', show_category_page_view, name='show-category'),

]

    