
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:profile_id>", views.profile, name='profile'),
    path('post', views.post, name='post'),

    # API Routes
    path('content/<int:post_id>', views.content, name='content'),
    path('follow/<int:user_id>', views.follow, name='follow'),
    path('get_follower/<int:user_id>', views.get_follower_count, name='get_follower'),
    path('like_post/<int:post_id>', views.like_post, name="like_post")
]
