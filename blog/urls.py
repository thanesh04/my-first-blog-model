from django.urls import path
from . import views

urlpatterns = [
    # Home page (list of posts)
    path('', views.post_list, name='post_list'),

    # Post detail page
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    #for like
    path('like/<int:pk>/', views.like_post, name='like_post'),
]