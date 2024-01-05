from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm
from .models import Account, UserFollowing, Posts, Like, Comment


def locationPost(request, location):
    posts = Posts.objects.filter(location__contains=location)
    print(posts)
    return render(request, "network/locations.html", {
        'location': location,
        'full_post': posts
    })


@login_required
def likeView(request, post_id):
    user = request.user
    post = Posts.objects.get(id=post_id)
    current_likes = post.likes.count()
    liked = Like.objects.filter(user=user, post=post).count()
    if not liked:
        liked = Like.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        liked = Like.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1

    post.likes.set(Account.objects.filter(liked_posts=post))
    post.save()
    return JsonResponse({'success': True, 'like_count': current_likes})


@login_required(login_url='login')
def home(request):
    user = request.user
    # Get the IDs of users that the current user is already following
    following_ids = UserFollowing.objects.filter(
        user=user).values_list('following_user__id', flat=True)
    # Get the first 6 users that the current user does not follow and exclude the current user
    customers = Account.objects.exclude(
        id__in=following_ids).exclude(id=user.id)[:6]

    posts_with_likes = []
    for post in Posts.objects.all():
        like_count = Like.objects.filter(post=post).count()
        liked = Like.objects.filter(post=post, user=user).exists()
        location = post.location.split(",")[0].strip()
        posts_with_likes.append(
            {'post': post, 'like_count': like_count, 'liked': liked, 'location': location})

    return render(request, "network/home.html", {
        'user': user,
        'customers': customers,
        'posts_with_likes': posts_with_likes,
    })


@login_required(login_url='login')
def add_comment(request, post_id):
    user = request.user
    post = get_object_or_404(Posts, pk=post_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text', '')
        if comment_text:
            Comment.objects.create(user=user, post=post, text=comment_text)

    return redirect('home')


def profile(request, username):
    customer = Account.objects.filter(username=username).first()
    user = request.user
    # Get the IDs of users that the current user is already following
    following_ids = UserFollowing.objects.filter(
        user=user).values_list('following_user__id', flat=True)

    return render(request, "network/profile.html", {
        'customer': customer,
        'following_ids': following_ids,
    })


def homePage(request):
    return render(request, "network/home.html", {
    })


def createPost(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["file"]
        location = request.POST["location"]

        Posts.objects.get_or_create(
            author=request.user, title=title, description=description, location=location, photo=image)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "network/create.html", {
        })


@login_required
def follow_user(request):
    user_id_to_follow = request.POST.get('user_id')
    user_to_follow = get_object_or_404(Account, id=user_id_to_follow)
    # Check if the user is not trying to follow themselves
    if user_to_follow != request.user:
        # Create a following relationship
        UserFollowing.objects.get_or_create(
            user=request.user, following_user=user_to_follow)

    return redirect('profile', user_to_follow.username)


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(Account, username=username)

    # Remove the following relationship
    UserFollowing.objects.filter(
        user=request.user, following_user=user_to_unfollow).delete()

    return redirect('profile', username)


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def signIn(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "network/signIn.html", {
                "message": "Please check your username and password."
            })
    return render(request, "network/signIn.html")


def registration(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    context = {}
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            if account is not None and account.pk is not None:
                login(request, account)
                destination = kwargs.get("next")
                if destination:
                    return redirect(destination)
            return HttpResponseRedirect(reverse("home"))
        else:
            context['registration_form'] = form

    return render(request, "network/registration.html", {
        'form': context,
    })
