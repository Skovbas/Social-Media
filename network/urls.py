from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('registration/', views.registration, name="registration"),
    path('login/', views.signIn, name="login"),
    path('logout', views.log_out, name="logout"),
    path('homepage/', views.homePage, name="homepage"),
    path('create/', views.createPost, name="create"),
    path('follow/', views.follow_user, name="follow"),
    path('unfollow/<str:username>/', views.unfollow_user, name="unfollow"),
    path('profile/<str:username>', views.profile, name="profile")
]
