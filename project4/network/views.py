from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from json import loads
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

from .models import User, Post
from .util import get_post
from json import dumps

@login_required
def index(request):
    return render(request, "network/index.html", {
        'posts': dumps([post.serialize() for post in Post.objects.all()])
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def profile(request, profile_id):
    user = get_object_or_404(User, pk=profile_id)
    return render(request, 'network/profile.html', {
        'base_user': user 
    })

@login_required
def post(request):
    if request.method == 'POST':
        print(request.POST['content'])
        Post.objects.create(writer=request.user, content=request.POST['content'])
    return HttpResponseRedirect(reverse('profile', args=[request.user.id]))

@login_required
@csrf_exempt
def like_post(request, post_id):
    print(request)
    post = get_post(post_id)
    if post is None:
        return JsonResponse({'error': "Post doesn't exist"}, status=404)
    
    user = request.user
    print(user)

    if(user in post.liked_users.all()):
        post.liked_users.remove(user)
    else:
        post.liked_users.add(user)
    
    return HttpResponse(status=204)


@login_required
@csrf_exempt
def content(request, post_id):

    # get the post from database
    print(request)
    post = get_post(post_id)
    if post is None:
        return JsonResponse({'error': "Post doesn't exist"}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({'content': post.content})
    
    data = loads(request.body)
    print(data['content'])
    post.content = data['content']
    post.save()
    return HttpResponse(status=204)
        


@login_required
@csrf_exempt
def follow(request, user_id):
    try:
        profile_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': "User doesn't exist"}, status=404)
    
    current_user = request.user

    if current_user in profile_user.followers.all():
        profile_user.followers.remove(current_user)
    else:
        profile_user.followers.add(current_user)

    # to see if the user has correctly followed or unfollowed...
    print(profile_user.followers.all(), profile_user.followings.all())
    return HttpResponse(status=204)

def get_follower_count(request, user_id):
    try:
        profile_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': "User doesn't exist"}, status=404)
    
    # if successful...
    return JsonResponse({'follower_count': profile_user.followers.count()})