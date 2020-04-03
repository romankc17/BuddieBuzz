from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Post, PostComment



@login_required
def like(request):
    user = request.user
    post = Post.objects.get(id=(request.POST.get('post_id')))
    is_liked=post.is_likedby(user)
    if is_liked:
        post.unlikedby(user)
    else:
        post.likedby(user)
    data={'is_liked':post.is_likedby(user),
          'countLike': str(post.likes.count()),
          }
    return JsonResponse(data)

@login_required
def post_comment(request):
    if request.method == 'POST' and request.is_ajax:
        print('till here')
        comment = request.POST.get('comment')

        post_slug = request.POST.get('post_slug')
        post = Post.objects.get(slug=post_slug)
        print(post)

        c = PostComment(body = comment,
                        commenter = request.user,
                        post  = post,
                        )
        c.save()
        data = {'commenter':request.user.username}

        return JsonResponse(data)