from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Admin panel
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return f'media_cdn/profile_images/{str(self.pk)}/{"profile_image.png"}'


def get_post_image_filepath(self, filename):
    return f'media_cdn/posts/{str(self.pk)}/{"post.png"}'


def get_default_profile_image():
    return "images/logo.jpeg"


class Account(AbstractBaseUser):
    email = models.EmailField(
        max_length=255, verbose_name="email", unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(
        max_length=255, upload_to=get_profile_image_filepath,
        null=True, blank=True, default=get_default_profile_image
    )
    hide_email = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_lable):
        return True

    def get_profile_image_filepath(self, filename):
        return f'media_cdn/profile_images/{str(self.pk)}/{"profile_image.png"}'

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]


# Following/Followers
class UserFollowing(models.Model):
    user = models.ForeignKey(
        Account, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(
        Account, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} follows {self.following_user}"

    class Meta:
        unique_together = ('user', 'following_user')


class Like(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"


# Comments
class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Posts', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.post.title}"


# Posts
class Posts(models.Model):
    title = models.CharField(max_length=255, unique=False)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    photo = models.ImageField(
        upload_to=get_post_image_filepath, null=True, blank=True)
    author = models.ForeignKey(
        Account, related_name='posts', on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(
        Account, through=Like, related_name='liked_posts')

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.likes.count()
