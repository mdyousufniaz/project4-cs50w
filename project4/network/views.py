from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from json import loads
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post
from .util import get_post

@login_required
def index(request):
    return render(request, "network/index.html", {
        'posts': Post.objects.all()
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

def like_post(request, post_id):
    print(request)
    post = get_post(post_id)
    if post is None:
        return JsonResponse({'error': "Post doesn't exist"}, status=404)
    
    user = request.user
    print(user)


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
    
    else:
        data = loads(request.body)
        print(data['content'])
        post.content = data['content']
        post.save()
        return HttpResponse(status=204)
        