from .models import Post

def get_post(post_id):

    try:
        post = Post.objects.get(pk=post_id)
        return post
    except Post.DoesNotExist:
        return None