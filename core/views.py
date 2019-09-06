from django.db.models import Sum
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core import exceptions
from core import models
from core.forms import PostForm


def index(request):
    post_queryset = models.Post.objects.annotate(like_nums=Sum('likes')).order_by('-like_nums')[:10]
    context = {
        'popular_posts': post_queryset
    }
    return render(request, 'core/index.html', context)


def feed(request):
    feed_queryset = models.Post.objects.filter(author__in=request.user.profile.friends.all())
    output = ["id:{}|description:{}\n".format(post.id, post.description) for post in feed_queryset]
    return HttpResponse(output)


def post_detail(request, post_id):
    post = get_object_or_404(models.Post, pk=post_id)
    return render(request, 'core/post_detail.html', {'post': post})


def post_delete(request, post_id):
    response = "Удаление поста #{}".format(post_id)
    return HttpResponse(response)


def post_edit(request, post_id):
    response = "Редактирование поста #{}".format(post_id)
    return HttpResponse(response)


def post_create(request):
    template_name = 'core/post_create.html'
    context = {'form': PostForm()}
    if request.method == "GET":
        return render(request=request, template_name=template_name, context=context)
    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.date_pub = timezone.now()
            post.author = request.user
            print(post)
            post.save()
            context['post_was_created'] = True
            return render(request=request, template_name=template_name, context=context)
        else:
            context['post_was_created'] = False
            context['form'] = form
            return render(request=request, template_name=template_name, context=context)


def like_post(request, post_id):
    post = get_object_or_404(models.Post, pk=post_id)
    if request.user in post.likes.all():
        like = post.likes.get(pk=request.user.id)
        post.likes.remove(like)
    else:
        post.likes.add(request.user)
        post.save()
    return redirect(request.META.get('HTTP_REFERER'), request)

