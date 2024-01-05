from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('registration', views.registration, name="registration"),
    path('login', views.signIn, name="login"),
    path('logout', views.log_out, name="logout"),
    path('homepage', views.homePage, name="homepage"),
    path('create', views.createPost, name="create"),
    path('follow', views.follow_user, name="follow"),
    path('unfollow/<str:username>', views.unfollow_user, name="unfollow"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('add_comment/<int:post_id>', views.add_comment, name='add_comment'),
    path('<int:post_id>/like', views.likeView, name='like'),
    path("location/<str:location>", views.locationPost, name="location"),
]
